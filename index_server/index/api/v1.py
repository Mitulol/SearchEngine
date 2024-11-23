"""General."""
import flask
import index
# import index_server #not sure if its server or index??


@index.app.route('/api/v1/', methods=['GET'])
def v1():
    """Get infor available."""
    context = {
         "hits": "/api/v1/hits/",
         "url": "/api/v1/"
    }

    return flask.jsonify(**context)