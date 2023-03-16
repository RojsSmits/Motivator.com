from website import  create_app
#parāda, kur darbosies mājaslapa un to palaiž
app=create_app()

if __name__=='__main__':
    app.run(debug=True, port=8000)
