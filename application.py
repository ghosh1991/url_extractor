"""  Application entry point """
from server.server import run_server


def start_application():
    """
    Start the rest application
    :return:
    """
    run_server()


if __name__ == "__main__":
    start_application()
