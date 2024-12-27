class Settings:
    def __init__(self):
        self.feature_toggles = {
            'role_based_channel_access': True,
            'logging': False,
        }

    def toggle_feature(self, feature_name):
        self.feature.toggles[feature_name] = not self.feature_toggles[feature_name]
        if feature_name in self.feature_toggles:
            return f'{feature_name} is now set to {self.feature_toggles[feature_name]}'
        return f'Feature {feature_name} does not exist'
    
    def is_feature_enabled(self, feature_name):
        return self.feature_toggles.get(feature_name, False)


