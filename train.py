from src.models.wrapper import DIETClassifierWrapper

config_file = "src/config.yml"
wrapper = DIETClassifierWrapper(config=config_file)

#predict
wrapper.predict(["How to check attendance?"])

#train
#after training, wrapper will load best model automatically
wrapper.train_model(save_folder="test_model")