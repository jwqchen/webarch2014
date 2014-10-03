#!/usr/bin/env python

import shelve
from subprocess import check_output
import flask
from flask import request
from os import environ

app = flask.Flask(__name__)
app.debug = True

#open "shoten.db" which is saved in harbinger under webarch/server
db = shelve.open("shorten.db")


###
# Home Resource:
# Only supports the GET method, returns a homepage represented as HTML
###
#when you go to /home, the def home() function runs
@app.route('/home', methods=['GET'])
def home():
    """Builds a template based on a GET request, with some default
    arguements"""
    #telnet/browser and URL something like this: http://www...../?title="..."&name="..."
    #"i253" is the default value if no title is entered
    index_title = request.args.get("title", "i253")
    hello_name = request.args.get("name", "Jim")
    return flask.render_template(
            #run the home.html stored in harbinger ./webarch/server
            #it's a template with html variables named "title" and "name"
            #you modify the value of title and name
            'home.html',
            title=index_title,
            name=hello_name)


###
# Wiki Resource:
# GET method will redirect to the resource stored by GET, by default: Wikipedia.org
# POST/PUT method will update the redirect destination in the database
###
@app.route('/wiki', methods=['GET'])

def wiki_get():
    """Redirects to wikipedia."""
    #get the value corresponding to the key 'wiki' in db, if nothing found, return 'http://en.wiki.org' as default)
    destination = db.get('wiki', 'http://en.wikipedia.org')
    app.logger.debug("Redirecting to " + destination)
    return flask.redirect(destination)

@app.route("/wiki", methods=['PUT', 'POST'])
def wiki_put():
    """Set or update the URL to which this resource redirects to. Uses the
    `url` key to set the redirect destination."""
    wikipedia = request.form.get('url', 'http://en.wikipedia.org')
    db['wiki'] = wikipedia
    return "Stored wiki => " + wikipedia

###
# i253 Resource:
# Information on the i253 class. Can be parameterized with `relationship`,
# `name`, and `adjective` information
#
# TODO: The representation for this resource is broken. Fix it!
# Set the correct MIME type to be able to view the image in your browser
##/
@app.route('/i253')
def i253():
    """Returns a PNG image of madlibs text"""
    relationship = request.args.get("relationship", "friend")
    name = request.args.get("name", "Jim")
    adjective = request.args.get("adjective", "fun")
    display_string = "My" +relationship+ " " +name+ "said i253 was" +adjective
    match = request.accept_mimetypes.best_match()

    accept_type = request.args.get('accept')
    
    resp_text = flask.make_response(display_string)
    resp_text.headers['Content-Type'] = 'text'


    resp_img = flask.make_response(
        #it's an image format below
        check_output(['convert', '-size', '600x400', 'xc:transparent',
            '-frame', '10x30',
            '-font', '/usr/share/fonts/liberation/LiberationSerif-BoldItalic.ttf',
            '-fill', 'black',
            '-pointsize', '32',
            '-draw',
              "text 30,60 'My %s %s said i253 was %s'" % (relationship, name, adjective),
            '-raise', '30',
            'png:-']), 200);
    # Comment in to set header below
    #write in image type below so the response sent back from the server has a header that's the same as "Content-Type". 
    #Then the receiving browser would know it's getting an image. 
    resp_img.headers['Content-Type'] = 'image'
    
    if (accept_type == "text"):
        return resp_text
    elif (accept_type == "image"):
        return resp_img
    elif (match == "text/plain"):
        return resp_text
    elif (match == "img/png"):
        return resp_img


if __name__ == "__main__":
    app.run(port=int(environ['FLASK_PORT']))
