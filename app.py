"""Student Result Service - sample application for the DevOps CI/CD lab (Batch A3)."""
import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

APP_VERSION = "1.1.0"


def average(marks):
    if not marks:
        raise ValueError("marks list is empty")
    return round(sum(marks) / len(marks), 2)


def grade(avg):
    if avg < 0 or avg > 100:
        raise ValueError("average must be between 0 and 100")
    if avg >= 85:
        return "O"
    if avg >= 75:
        return "A"
    if avg >= 60:
        return "B"
    if avg >= 40:
        return "C"
    return "F"


def result(name, marks):
    avg = average(marks)
    return {"name": name, "average": avg, "grade": grade(avg), "passed": avg >= 40,
            "distinction": avg >= 75}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            body = {"status": "UP", "version": APP_VERSION}
        else:
            body = {"app": "student-result-service", "version": APP_VERSION,
                    "sample": result("Vansh", [82, 91, 77, 88])}
        data = json.dumps(body).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(data)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "serve":
        print("Serving on :8000", flush=True)
        HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
    else:
        print("Build check OK - version", APP_VERSION)
        print(result("Vansh", [82, 91, 77, 88]))
