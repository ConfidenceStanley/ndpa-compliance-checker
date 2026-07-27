from flask import Flask
from flask_login import LoginManager
from models import db
from models.user import User
from config import Config
import json
import os

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'

    from routes.auth import auth
    from routes.dashboard import dashboard
    from routes.compliance import compliance
    from routes.history import history
    from routes.admin import admin

    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(compliance)
    app.register_blueprint(history)
    app.register_blueprint(admin)

    with app.app_context():
        from models.compliance import NdpaRule, ComplianceReport
        db.create_all()
        seed_ndpa_rules(app)

    return app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def seed_ndpa_rules(app):
    from models.compliance import NdpaRule
    with app.app_context():
        if NdpaRule.query.count() == 0:
            rules_path = os.path.join(os.path.dirname(__file__), 'data', 'ndpa_rules.json')
            with open(rules_path, 'r') as f:
                rules = json.load(f)
            for rule in rules:
                new_rule = NdpaRule(
                    section=rule['section'],
                    rule_text=rule['rule_text'],
                    rule_type=rule['rule_type']
                )
                db.session.add(new_rule)
            db.session.commit()
            print(f"Seeded {len(rules)} NDPA rules into database.")
        else:
            print("NDPA rules already seeded.")


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)