from TaskMan import create_app

if __name__ == '__main__':
    app = create_app('DEV')
    app.run(port=8000)