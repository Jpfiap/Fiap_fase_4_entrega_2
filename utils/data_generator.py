import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random


class SensorDataGenerator:
    """
    Gerador de dados simulados para sensores do sistema de irrigação.
    Simula leituras realistas baseadas em padrões de cultivo de milho.
    """

    def __init__(self):
        self.base_humidity = 50  # Umidade base
        self.base_ph = 6.5  # pH base
        self.base_phosphorus = 25  # Fósforo base em ppm
        self.base_potassium = 150  # Potássio base em ppm

        # Variações para simular condições naturais
        self.humidity_variation = 10
        self.ph_variation = 0.3
        self.phosphorus_variation = 5
        self.potassium_variation = 20

        # Padrões sazonais e diários
        self.time_factor = 0

    def _get_time_factor(self, timestamp=None):
        """
        Calcula fator de tempo para simular variações naturais.
        """
        if timestamp is None:
            timestamp = datetime.now()

        # Fator diário (umidade maior de manhã)
        hour_factor = np.sin(2 * np.pi * timestamp.hour / 24) * 0.1

        # Fator semanal (simulando ciclo de irrigação)
        day_factor = np.sin(2 * np.pi * timestamp.weekday() / 7) * 0.05

        return hour_factor + day_factor

    def _add_realistic_noise(self, value, noise_level=0.02):
        """
        Adiciona ruído realista para simular variações dos sensores.
        """
        noise = np.random.normal(0, noise_level * value)
        return value + noise

    def generate_current_reading(self, timestamp=None):
        """
        Gera uma leitura atual dos sensores.

        Returns:
            dict: dados atuais dos sensores
        """
        if timestamp is None:
            timestamp = datetime.now()

        time_factor = self._get_time_factor(timestamp)

        # Gerar umidade com variações naturais
        humidity = self.base_humidity + (time_factor * 20) + \
                   np.random.normal(0, self.humidity_variation)
        humidity = np.clip(humidity, 15, 85)
        humidity = self._add_realistic_noise(humidity)

        # Gerar pH com menor variação
        ph = self.base_ph + np.random.normal(0, self.ph_variation)
        ph = np.clip(ph, 5.5, 8.0)
        ph = self._add_realistic_noise(ph, 0.01)

        # Gerar fósforo com variação gradual
        phosphorus = self.base_phosphorus + np.random.normal(0, self.phosphorus_variation)
        phosphorus = np.clip(phosphorus, 5, 50)
        phosphorus = self._add_realistic_noise(phosphorus)

        # Gerar potássio com variação gradual
        potassium = self.base_potassium + np.random.normal(0, self.potassium_variation)
        potassium = np.clip(potassium, 80, 250)
        potassium = self._add_realistic_noise(potassium)

        return {
            'timestamp': timestamp,
            'humidity': float(humidity),
            'ph': float(ph),
            'phosphorus': float(phosphorus),
            'potassium': float(potassium),
            'temperature': float(np.random.normal(25, 3)),  # Temperatura ambiente
            'light_intensity': float(np.random.normal(50, 10))  # Intensidade luminosa
        }

    def generate_historical_data(self, hours=24, frequency_minutes=30):
        """
        Gera dados históricos para um período específico.

        Args:
            hours: número de horas para gerar dados
            frequency_minutes: frequência em minutos entre leituras

        Returns:
            pandas.DataFrame: dados históricos
        """
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours)

        # Gerar timestamps
        timestamps = pd.date_range(
            start=start_time,
            end=end_time,
            freq=f'{frequency_minutes}min'
        )

        historical_data = []

        for timestamp in timestamps:
            reading = self.generate_current_reading(timestamp)
            historical_data.append(reading)

        df = pd.DataFrame(historical_data)

        # Adicionar tendências realistas
        df = self._add_realistic_trends(df)

        return df

    def _add_realistic_trends(self, df):
        """
        Adiciona tendências realistas aos dados históricos.
        """
        # Simular depleção gradual de umidade
        hours_passed = (df['timestamp'] - df['timestamp'].iloc[0]).dt.total_seconds() / 3600
        humidity_trend = -0.5 * hours_passed  # Perda de 0.5% por hora
        df['humidity'] = df['humidity'] + humidity_trend
        df['humidity'] = df['humidity'].clip(15, 85)

        # Simular variação de pH mais estável
        df['ph'] = df['ph'] + np.random.normal(0, 0.05, len(df))
        df['ph'] = df['ph'].clip(5.5, 8.0)

        # Simular depleção gradual de nutrientes
        nutrient_trend = -0.1 * hours_passed  # Perda gradual
        df['phosphorus'] = df['phosphorus'] + nutrient_trend
        df['potassium'] = df['potassium'] + nutrient_trend * 2

        df['phosphorus'] = df['phosphorus'].clip(5, 50)
        df['potassium'] = df['potassium'].clip(80, 250)

        return df

    def simulate_irrigation_event(self, pre_irrigation_data, duration_hours=2):
        """
        Simula os efeitos de um evento de irrigação nos dados dos sensores.

        Args:
            pre_irrigation_data: dados antes da irrigação
            duration_hours: duração do efeito da irrigação

        Returns:
            dict: dados após irrigação
        """
        post_irrigation_data = pre_irrigation_data.copy()

        # Aumento da umidade
        humidity_increase = np.random.uniform(15, 25)
        post_irrigation_data['humidity'] = min(85,
                                               pre_irrigation_data['humidity'] + humidity_increase)

        # Leve alteração no pH devido à diluição
        ph_change = np.random.uniform(-0.1, 0.1)
        post_irrigation_data['ph'] = np.clip(
            pre_irrigation_data['ph'] + ph_change, 5.5, 8.0)

        # Leve diluição dos nutrientes
        nutrient_dilution = np.random.uniform(0.95, 0.98)
        post_irrigation_data['phosphorus'] *= nutrient_dilution
        post_irrigation_data['potassium'] *= nutrient_dilution

        post_irrigation_data['timestamp'] = datetime.now()

        return post_irrigation_data

    def get_sensor_status(self, reading):
        """
        Determina o status dos sensores baseado na leitura atual.

        Args:
            reading: dicionário com dados dos sensores

        Returns:
            dict: status de cada sensor
        """
        status = {}

        # Status da umidade
        if reading['humidity'] < 30:
            status['humidity'] = 'CRÍTICO'
        elif reading['humidity'] < 45:
            status['humidity'] = 'BAIXO'
        elif reading['humidity'] > 75:
            status['humidity'] = 'ALTO'
        else:
            status['humidity'] = 'NORMAL'

        # Status do pH
        if reading['ph'] < 6.0 or reading['ph'] > 7.5:
            status['ph'] = 'FORA DO RANGE'
        else:
            status['ph'] = 'NORMAL'

        # Status do fósforo
        if reading['phosphorus'] < 15:
            status['phosphorus'] = 'BAIXO'
        elif reading['phosphorus'] > 35:
            status['phosphorus'] = 'ALTO'
        else:
            status['phosphorus'] = 'NORMAL'

        # Status do potássio
        if reading['potassium'] < 120:
            status['potassium'] = 'BAIXO'
        elif reading['potassium'] > 200:
            status['potassium'] = 'ALTO'
        else:
            status['potassium'] = 'NORMAL'

        return status

    def generate_alert_conditions(self, probability=0.1):
        """
        Gera condições que podem gerar alertas no sistema.

        Args:
            probability: probabilidade de gerar condição de alerta

        Returns:
            dict: dados com possível condição de alerta
        """
        reading = self.generate_current_reading()

        if np.random.random() < probability:
            # Simular condição de alerta
            alert_type = np.random.choice(['humidity', 'ph', 'nutrients'])

            if alert_type == 'humidity':
                reading['humidity'] = np.random.uniform(15, 35)
            elif alert_type == 'ph':
                reading['ph'] = np.random.choice([
                    np.random.uniform(5.0, 5.8),
                    np.random.uniform(7.8, 8.5)
                ])
            elif alert_type == 'nutrients':
                reading['phosphorus'] = np.random.uniform(5, 12)
                reading['potassium'] = np.random.uniform(80, 110)

        return reading
