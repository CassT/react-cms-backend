from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from models import session, Page
from flask_cors import CORS


app = Flask(__name__)
api = Api(app)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

parser = reqparse.RequestParser()
parser.add_argument('path')
parser.add_argument('title')
parser.add_argument('content')


class SinglePage(Resource):
    def get(self, page_id):
        page_model = session.query(Page).get(page_id)
        if page_model is not None:
            return page_model.as_dictionary()
        else:
            return None

    def put(self, page_id):
        args = parser.parse_args()
        page_model = session.query(Page).get(page_id)
        if page_model is not None:
            page_model.slug = args['slug']  # No validation confirming that this isn't present
            page_model.title = args['title']
            page_model.content = args['content']
            session.commit()
            return page_model.as_dictionary()
        else:
            return None

    def delete(self, page_id):
        page_model = session.query(Page).get(page_id)
        if page_model is not None and page_id != -1:
            #print(page_model.as_dictionary())
            session.delete(page_model)
            session.commit()
            return "success"
        else:
            return None


class Pages(Resource):
    def get(self):
        return [
            page_model.as_dictionary() for page_model in session.query(Page).all()
        ]

    def post(self):
        args = parser.parse_args()
        new_page = Page(
            title=args["title"],
            parent=args["parent"],
            slug=args["slug"],
            content=args["content"]
        )
        # Ensure slug/title pair is not present
        if not session.query(Page).filter_by(parent=new_page.parent, slug=new_page.slug).count() and new_page.title:
            session.add(new_page)
            session.commit()
            return new_page.as_dictionary()
        else:
            return None


class Navigation(Resource):
    def get(self):
        return [
            {
                "title": page_model.title,
                "slug": page_model.slug,
            } for page_model in session.query(Page).filter_by(parent=-1)
        ]


class PageNavigation(Resource):
    def get(self, page_id):
        children = session.query(Page).filter_by(parent=page_id)
        return [child.navigation_dictionary() for child in children]

api.add_resource(SinglePage, '/page/<int:page_id>/')
api.add_resource(Pages, '/page')
api.add_resource(Navigation, '/navigation')
api.add_resource(PageNavigation, '/navigation/<int:page_id>')
