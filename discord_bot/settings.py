class Settings:
    ''' Class to manage feature toggles. '''
    def __init__(self):
        self.feature_toggles = {
            'role_based_channel_access': True,
            'logging': False,
            'easter_eggs': True,
            'ollama': True,
            'music_requests': False,
            'welcome_message': True,
        }

    def toggle_feature(self, feature_name):
        ''' Toggle a feature on or off. '''
        self.feature_toggles[feature_name] = not self.feature_toggles[feature_name]
        if feature_name in self.feature_toggles:
            return f'{feature_name} is now set to {self.feature_toggles[feature_name]}'
        return f'Feature {feature_name} does not exist'
    
    def is_feature_enabled(self, feature_name):
        ''' Check if a feature is enabled. '''
        return self.feature_toggles.get(feature_name, False)
