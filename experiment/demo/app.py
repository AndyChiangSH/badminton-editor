from flask import Flask, render_template, request
import pandas
import json
from pipeline import preprocess, translate, generate_answer, generate_news


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/pipeline", methods=["GET", "POST"])
def pipeline():
    if request.method == "GET":
        return "Pipeline OK!"
    else:        
        try:
            # print(f"Get data...")
            file = request.files["file"]
            model = request.values["model"]
            # print("file:", file)
            # print("model:", model)
        except:
            response = {
                "state": "fail",
                "content": "Get data"
            }
            return response
        
        try:
            # print(f"Read file...")
            input_df = pandas.read_csv(file)
            # print("input_df:", input_df)
        except:
            response = {
                "state": "fail",
                "content": "Read file"
            }
            return response
        
        try:
            # print(f"Preprocess...")
            preprocessed_df = preprocess(input_df)
            # print("preprocessed_df:", preprocessed_df)
        except:
            response = {
                "state": "fail",
                "content": "Preprocess"
            }
            return response

        try:
            # print("Translate...")
            translated_df = translate(preprocessed_df)
            # print("translated_df:", translated_df)
        except:
            response = {
                "state": "fail",
                "content": "Translate"
            }
            return response
        
        try:
            # print("Generate answer...")
            answers = generate_answer(translated_df)
            # print("answers:", answers)
        except:
            response = {
                "state": "fail",
                "content": "Generate answer"
            }
            return response

        try:
            # print("Generate news...")
            news = generate_news(answers, model)
            # print("news:", news)
        except:
            response = {
                "state": "fail",
                "content": "Generate news"
            }
            return response
        
        response = {
            "state": "success",
            "content": news
        }
        
        return response


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host="0.0.0.0")