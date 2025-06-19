import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
import joblib
import os


class IrrigationModel:
    """
    Modelo preditivo para sistema de irrigação automatizada de milho.
    Usa Random Forest para predizer necessidade de irrigação baseado em:
    - Umidade do solo (%)
    - pH do solo
    - Níveis de fósforo (ppm)
    - Níveis de potássio (ppm)
    """

    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = ['humidity', 'ph', 'phosphorus', 'potassium']
        self.is_trained = False
        self._train_model()

    def _generate_training_data(self, n_samples=1000):
        """
        Gera dados de treinamento baseados em características ideais do milho.
        """
        np.random.seed(42)  # Para reprodutibilidade

        # Gerar features baseadas em condições reais para milho
        humidity = np.random.normal(50, 15, n_samples)  # Umidade média 50%
        humidity = np.clip(humidity, 15, 85)  # Limitar range realista

        ph = np.random.normal(6.5, 0.5, n_samples)  # pH ideal 6.0-7.0
        ph = np.clip(ph, 5.5, 8.0)

        phosphorus = np.random.normal(25, 10, n_samples)  # Fósforo em ppm
        phosphorus = np.clip(phosphorus, 5, 50)

        potassium = np.random.normal(150, 30, n_samples)  # Potássio em ppm
        potassium = np.clip(potassium, 80, 250)

        # Criar labels baseados em regras agronômicas
        irrigation_needed = np.zeros(n_samples)

        for i in range(n_samples):
            score = 0

            # Umidade baixa = precisa irrigar
            if humidity[i] < 40:
                score += 3
            elif humidity[i] < 50:
                score += 1
            elif humidity[i] > 70:
                score -= 2

            # pH fora do range ideal
            if ph[i] < 6.0 or ph[i] > 7.0:
                score += 1

            # Nutrientes baixos podem indicar necessidade de irrigação
            if phosphorus[i] < 15:
                score += 1
            if potassium[i] < 120:
                score += 1

            # Condições extremas
            if humidity[i] < 30:
                score += 2

            # Adicionar ruído para tornar mais realista
            score += np.random.normal(0, 0.5)

            # Converter score para decisão binária
            irrigation_needed[i] = 1 if score > 1.5 else 0

        # Criar DataFrame
        data = pd.DataFrame({
            'humidity': humidity,
            'ph': ph,
            'phosphorus': phosphorus,
            'potassium': potassium,
            'irrigation_needed': irrigation_needed
        })

        return data

    def _train_model(self):
        """
        Treina o modelo com dados sintéticos baseados em conhecimento agronômico.
        """
        # Gerar dados de treinamento
        training_data = self._generate_training_data(1000)

        # Preparar features e target
        X = training_data[self.feature_names]
        y = training_data['irrigation_needed']

        # Dividir dados
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        # Escalar features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        # Treinar modelo
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        )

        self.model.fit(X_train_scaled, y_train)

        # Avaliar modelo
        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)

        self.is_trained = True
        print(f"Modelo treinado com acurácia: {accuracy:.3f}")

    def predict(self, features):
        """
        Prediz se irrigação é necessária.

        Args:
            features: array-like, shape (n_samples, 4)
                     [humidity, ph, phosphorus, potassium]

        Returns:
            array: predições (0 = não irrigar, 1 = irrigar)
        """
        if not self.is_trained:
            raise ValueError("Modelo não foi treinado ainda")

        features_scaled = self.scaler.transform(features)
        return self.model.predict(features_scaled)

    def predict_proba(self, features):
        """
        Prediz probabilidades de irrigação.

        Args:
            features: array-like, shape (n_samples, 4)

        Returns:
            array: probabilidades [prob_não_irrigar, prob_irrigar]
        """
        if not self.is_trained:
            raise ValueError("Modelo não foi treinado ainda")

        features_scaled = self.scaler.transform(features)
        return self.model.predict_proba(features_scaled)

    def get_feature_importance(self):
        """
        Retorna a importância das features.

        Returns:
            dict: importância de cada feature
        """
        if not self.is_trained:
            raise ValueError("Modelo não foi treinado ainda")

        importances = self.model.feature_importances_

        return {
            'Umidade': importances[0],
            'pH': importances[1],
            'Fósforo': importances[2],
            'Potássio': importances[3]
        }

    def get_recommendations(self, sensor_data):
        """
        Gera recomendações baseadas nos dados dos sensores.

        Args:
            sensor_data: dict com dados dos sensores

        Returns:
            list: lista de recomendações
        """
        recommendations = []

        # Análise de umidade
        if sensor_data['humidity'] < 35:
            recommendations.append("🚨 Irrigação urgente necessária - umidade crítica")
        elif sensor_data['humidity'] < 45:
            recommendations.append("💧 Considere irrigação - umidade baixa")
        elif sensor_data['humidity'] > 75:
            recommendations.append("⚠️ Umidade alta - verifique drenagem")

        # Análise de pH
        if sensor_data['ph'] < 6.0:
            recommendations.append("🧪 Solo ácido - considere calcário")
        elif sensor_data['ph'] > 7.5:
            recommendations.append("🧪 Solo alcalino - considere enxofre")
        else:
            recommendations.append("✅ pH ideal para milho")

        # Análise de nutrientes
        if sensor_data['phosphorus'] < 15:
            recommendations.append("🌱 Fósforo baixo - aplicar fertilizante fosfatado")
        if sensor_data['potassium'] < 120:
            recommendations.append("🌱 Potássio baixo - aplicar fertilizante potássico")

        # Recomendação geral
        if sensor_data['humidity'] > 45 and 6.0 <= sensor_data['ph'] <= 7.0:
            recommendations.append("🌽 Condições ideais para desenvolvimento do milho")

        return recommendations if recommendations else ["✅ Condições adequadas - monitoramento contínuo"]

    def save_model(self, filepath):
        """
        Salva o modelo treinado.

        Args:
            filepath: caminho para salvar o modelo
        """
        if not self.is_trained:
            raise ValueError("Modelo não foi treinado ainda")

        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'feature_names': self.feature_names
        }

        joblib.dump(model_data, filepath)

    def load_model(self, filepath):
        """
        Carrega um modelo salvo.

        Args:
            filepath: caminho do modelo salvo
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Arquivo {filepath} não encontrado")

        model_data = joblib.load(filepath)

        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.feature_names = model_data['feature_names']
        self.is_trained = True
