import argparse


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="converting natural language to sql")
    # give the filename
    parser.add_argument("--train file", dest="train_file", default="", help="")
    