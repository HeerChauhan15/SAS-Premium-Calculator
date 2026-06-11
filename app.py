from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import os

GST_RATE = 0.18


def calc_premiums(sum_assured: float, rate: float):
    premium_inc_gst = (sum_assured * rate) / 100000.0
    premium_ex_gst = premium_inc_gst / (1 + GST_RATE)
    return premium_ex_gst, premium_inc_gst


def format_inr(value: float) -> str:
    return f"₹{value:,.2f}"


FORM_HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>GTL Premium Calculator</title>
</head>
<body style="font-family: Arial; padding: 20px;">

  <h2>GTL Premium Calculator</h2>

  <form method="POST">
    <label>Sum Assured</label><br>
    <input type="number" name="sumAssured" required><br><br>

    <!-- FIXED RATE -->
    <input type="hidden" name="rate" value="650">

    <button type="submit">Calculate</button>
  </form>

  <p>Rate is fixed at 650 (GST inclusive)</p>

</body>
</html>
"""


def render_result(ex_gst, inc_gst):
    return f"""
    <html>
    <body style="font-family: Arial; padding: 20px;">
        <h2>Result</h2>
        <p>Premium (Ex GST): <b>{format_inr(ex_gst)}</b></p>
        <p>Premium (Inc GST): <b>{format_inr(inc_gst)}</b></p>
        <br>
        <a href="/">Back</a>
    </body>
    </html>
    """


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(FORM_HTML.encode())

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        data = self.rfile.read(length).decode()
        params = parse_qs(data)

        sum_assured = float(params.get("sumAssured", [0])[0])

        # FIXED RATE ONLY
        rate = 650.0

        ex, inc = calc_premiums(sum_assured, rate)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(render_result(ex, inc).encode())


def main():
    host = "0.0.0.0"
    port = int(os.environ.get("PORT", 8000))

    server = HTTPServer((host, port), Handler)
    print(f"Running on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()