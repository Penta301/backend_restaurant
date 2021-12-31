import cloudinary.uploader
#Los datos a continuacion, deberan ser cambiados a variables de entorno en el deploy
cloudinary.config(
    cloud_name = 'smartrestaurantapi',
    api_key = "789184643458223", 
    api_secret = "mv0Dzw7fBAB3wZEwVCa80XFoPo8",
    secure = True
)

uploader = cloudinary.uploader
