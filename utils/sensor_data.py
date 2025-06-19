import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os


class SensorData:
    """
    Classe para gerenciar dados dos sensores, incluindo armazenamento,
    recuperação e análise de dados históricos.
    """

    def __init__(self, data_file="sensor_data.json"):
        self.data_file = data_file
        self.current_session_data = []
        self.load_data()

    def load_data(self):
        """
        Carrega dados históricos do arquivo.
        """
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.historical_data = data.get('historical_data', [])
                    self.irrigation_events = data.get('irrigation_events', [])
                    self.system_alerts = data.get('system_alerts', [])
            except Exception as e:
                print(f"Erro ao carregar dados: {e}")
                self._initialize_empty_data()
        else:
            self._initialize_empty_data()

    def _initialize_empty_data(self):
        """
        Inicializa estruturas de dados vazias.
        """
        self.historical_data = []
        self.irrigation_events = []
        self.system_alerts = []

    def save_data(self):
        """
        Salva dados no arquivo.
        """
        data = {
            'historical_data': self.historical_data,
            'irrigation_events': self.irrigation_events,
            'system_alerts': self.system_alerts,
            'last_updated': datetime.now().isoformat()
        }

        try:
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")

    def add_sensor_reading(self, reading):
        """
        Adiciona uma nova leitura dos sensores.

        Args:
            reading: dicionário com dados dos sensores
        """
        # Converter timestamp para string se necessário
        if isinstance(reading.get('timestamp'), datetime):
            reading['timestamp'] = reading['timestamp'].isoformat()

        self.historical_data.append(reading)
        self.current_session_data.append(reading)

        # Manter apenas os últimos 1000 registros
        if len(self.historical_data) > 1000:
            self.historical_data = self.historical_data[-1000:]

    def add_irrigation_event(self, event_type, details=None):
        """
        Registra um evento de irrigação.

        Args:
            event_type: tipo do evento ('start', 'stop', 'manual', 'auto')
            details: detalhes adicionais do evento
        """
        event = {
            'timestamp': datetime.now().isoformat(),
            'type': event_type,
            'details': details or {}
        }

        self.irrigation_events.append(event)

        # Manter apenas os últimos 100 eventos
        if len(self.irrigation_events) > 100:
            self.irrigation_events = self.irrigation_events[-100:]

    def add_system_alert(self, alert_type, message, severity='warning'):
        """
        Adiciona um alerta do sistema.

        Args:
            alert_type: tipo do alerta
            message: mensagem do alerta
            severity: severidade ('info', 'warning', 'critical')
        """
        alert = {
            'timestamp': datetime.now().isoformat(),
            'type': alert_type,
            'message': message,
            'severity': severity
        }

        self.system_alerts.append(alert)

        # Manter apenas os últimos 50 alertas
        if len(self.system_alerts) > 50:
            self.system_alerts = self.system_alerts[-50:]

    def get_recent_data(self, hours=24):
        """
        Obtém dados recentes dos sensores.

        Args:
            hours: número de horas para buscar

        Returns:
            list: dados dos sensores das últimas N horas
        """
        cutoff_time = datetime.now() - timedelta(hours=hours)

        recent_data = []
        for reading in self.historical_data:
            timestamp = reading['timestamp']
            if isinstance(timestamp, str):
                timestamp = datetime.fromisoformat(timestamp)

            if timestamp >= cutoff_time:
                recent_data.append(reading)

        return recent_data

    def get_sensor_statistics(self, hours=24):
        """
        Calcula estatísticas dos sensores.

        Args:
            hours: período para calcular estatísticas

        Returns:
            dict: estatísticas dos sensores
        """
        recent_data = self.get_recent_data(hours)

        if not recent_data:
            return {}

        df = pd.DataFrame(recent_data)

        # Converter colunas numéricas
        numeric_columns = ['humidity', 'ph', 'phosphorus', 'potassium']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        statistics = {}

        for col in numeric_columns:
            if col in df.columns:
                statistics[col] = {
                    'mean': float(df[col].mean()),
                    'min': float(df[col].min()),
                    'max': float(df[col].max()),
                    'std': float(df[col].std()),
                    'median': float(df[col].median())
                }

        return statistics

    def get_irrigation_summary(self, days=7):
        """
        Obtém resumo dos eventos de irrigação.

        Args:
            days: número de dias para resumir

        Returns:
            dict: resumo dos eventos de irrigação
        """
        cutoff_time = datetime.now() - timedelta(days=days)

        recent_events = []
        for event in self.irrigation_events:
            timestamp = event['timestamp']
            if isinstance(timestamp, str):
                timestamp = datetime.fromisoformat(timestamp)

            if timestamp >= cutoff_time:
                recent_events.append(event)

        summary = {
            'total_events': len(recent_events),
            'start_events': len([e for e in recent_events if e['type'] == 'start']),
            'stop_events': len([e for e in recent_events if e['type'] == 'stop']),
            'manual_events': len([e for e in recent_events if e['type'] == 'manual']),
            'auto_events': len([e for e in recent_events if e['type'] == 'auto']),
            'recent_events': recent_events[-10:]  # Últimos 10 eventos
        }

        return summary

    def get_active_alerts(self, hours=24):
        """
        Obtém alertas ativos (recentes).

        Args:
            hours: período para considerar alertas ativos

        Returns:
            list: alertas ativos
        """
        cutoff_time = datetime.now() - timedelta(hours=hours)

        active_alerts = []
        for alert in self.system_alerts:
            timestamp = alert['timestamp']
            if isinstance(timestamp, str):
                timestamp = datetime.fromisoformat(timestamp)

            if timestamp >= cutoff_time:
                active_alerts.append(alert)

        return active_alerts

    def analyze_trends(self, parameter, hours=24):
        """
        Analisa tendências de um parâmetro específico.

        Args:
            parameter: parâmetro para analisar ('humidity', 'ph', etc.)
            hours: período para análise

        Returns:
            dict: análise de tendência
        """
        recent_data = self.get_recent_data(hours)

        if not recent_data or len(recent_data) < 2:
            return {'trend': 'insufficient_data', 'change': 0}

        df = pd.DataFrame(recent_data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')

        if parameter not in df.columns:
            return {'trend': 'parameter_not_found', 'change': 0}

        # Calcular tendência linear
        values = df[parameter].values
        x = np.arange(len(values))

        # Regressão linear simples
        slope = np.polyfit(x, values, 1)[0]

        # Determinar tendência
        if abs(slope) < 0.1:
            trend = 'stable'
        elif slope > 0:
            trend = 'increasing'
        else:
            trend = 'decreasing'

        # Calcular mudança percentual
        if len(values) > 1:
            change_percent = ((values[-1] - values[0]) / values[0]) * 100
        else:
            change_percent = 0

        return {
            'trend': trend,
            'slope': float(slope),
            'change_percent': float(change_percent),
            'current_value': float(values[-1]) if len(values) > 0 else 0,
            'initial_value': float(values[0]) if len(values) > 0 else 0
        }

    def export_data(self, format='csv', filename=None):
        """
        Exporta dados em diferentes formatos.

        Args:
            format: formato de exportação ('csv', 'json', 'excel')
            filename: nome do arquivo (opcional)

        Returns:
            str: caminho do arquivo exportado
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'sensor_data_export_{timestamp}'

        if format == 'csv':
            df = pd.DataFrame(self.historical_data)
            filepath = f'{filename}.csv'
            df.to_csv(filepath, index=False)

        elif format == 'json':
            filepath = f'{filename}.json'
            with open(filepath, 'w') as f:
                json.dump({
                    'historical_data': self.historical_data,
                    'irrigation_events': self.irrigation_events,
                    'system_alerts': self.system_alerts
                }, f, indent=2, default=str)

        elif format == 'excel':
            filepath = f'{filename}.xlsx'
            with pd.ExcelWriter(filepath) as writer:
                pd.DataFrame(self.historical_data).to_excel(
                    writer, sheet_name='Sensor_Data', index=False)
                pd.DataFrame(self.irrigation_events).to_excel(
                    writer, sheet_name='Irrigation_Events', index=False)
                pd.DataFrame(self.system_alerts).to_excel(
                    writer, sheet_name='System_Alerts', index=False)

        return filepath

    def cleanup_old_data(self, days=30):
        """
        Remove dados antigos para economizar espaço.

        Args:
            days: manter dados dos últimos N dias
        """
        cutoff_time = datetime.now() - timedelta(days=days)

        # Filtrar dados históricos
        self.historical_data = [
            reading for reading in self.historical_data
            if datetime.fromisoformat(reading['timestamp']) >= cutoff_time
        ]

        # Filtrar eventos de irrigação
        self.irrigation_events = [
            event for event in self.irrigation_events
            if datetime.fromisoformat(event['timestamp']) >= cutoff_time
        ]

        # Filtrar alertas (manter apenas 7 dias)
        alert_cutoff = datetime.now() - timedelta(days=7)
        self.system_alerts = [
            alert for alert in self.system_alerts
            if datetime.fromisoformat(alert['timestamp']) >= alert_cutoff
        ]

        # Salvar dados limpos
        self.save_data()
