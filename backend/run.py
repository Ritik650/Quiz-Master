from app import create_app

app = create_app()
# from app.urls import register_routes
# register_routes(app)
from app.tasks import export_user_csv
app.add_url_rule('/api/user/export-data', view_func=export_user_csv, methods=['POST'])
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
