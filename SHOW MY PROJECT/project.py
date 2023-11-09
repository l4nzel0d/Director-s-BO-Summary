from dotenv import load_dotenv
import requests
import json
import re
from fpdf import FPDF
from PIL import Image
import urllib.request
from fpdf.enums import XPos
import re
from matplotlib import pyplot as plt
import os

load_dotenv('.env')

api_key: str = os.getenv('API_KEY')


class PDF(FPDF):
    def __init__(
        self,
        director_name,
        image_link,
        directed_pics,
        orientation="portrait",
        unit="mm",
        format="A4",
        font_cache_dir="DEPRECATED",
    ):
        super().__init__()
        self.director_name = director_name
        self.image_link = image_link
        self.directed_pics = sorted(
            directed_pics, key=lambda movie: movie["XWWgross"]["amount"], reverse=True
        )
        self.number_of_features = len(directed_pics)
        self.data = self.directed_pics
        self.set_left_margin(12)
        self.set_right_margin(12)

    def header(self):
        self.set_font("Courier", "BI", 32)
        self.cell(0, 10, "Box Office Summary", align="C")
        self.image(self.image_link, 12, 36, 48)
        # print first name
        x_start_of_name_box = 65
        self.set_y(43)
        self.set_x(x_start_of_name_box)
        self.set_font("Helvetica", "B", 45)
        first, last = re.fullmatch(r"(.*) (.*)", self.director_name).groups()
        name_box_width = 210 - 10 - 65
        self.cell(name_box_width, 0, first)
        # print last name
        self.set_y(57)
        self.set_x(x_start_of_name_box)
        self.cell(name_box_width, 0, last)
        # print "as Director"
        self.set_y(70)
        self.set_x(x_start_of_name_box)
        self.set_font("Helvetica", "I", 24)
        self.cell(0, 0, "as Director")
        # print line
        self.line(x_start_of_name_box + 2, 76, 198, 76)
        # print "Total Worldwide Box Office:"
        self.set_y(85)
        self.set_x(x_start_of_name_box)
        self.set_font("Helvetica", "", 22)
        self.cell(0, 0, "Total Worldwide Box Office:")
        # print value of total worldwide box office
        self.set_y(94)
        self.set_x(x_start_of_name_box)
        self.set_font("Helvetica", "B", 22)
        self.cell(0, 0, f"${self.total_WW():,}")
        # line
        self.ln(20)

    def footer(self):
        self.set_y(288)
        self.line(88, 289, 122, 289)
        self.set_font("courier", "b", 13)
        self.set_y(290)
        self.set_x(20)
        self.cell(0, 4, f"Page {self.page_no()}/{{nb}}", align="C")

    def total_WW(self):
        total = 0
        for movie in self.directed_pics:
            total += movie["XWWgross"]["amount"]
        return total

    def total_DOM(self):
        total = 0
        for movie in self.directed_pics:
            total += movie["XDOMgross"]["amount"]
        return total

    def total_NDOM(self):
        return self.total_WW() - self.total_DOM()

    def top_movies_getter(self):
        self.highest_grossing_worldwide_movie = self.directed_pics[0]
        self.highest_grossing_domestically_movie = sorted(
            self.directed_pics,
            key=lambda movie: movie["XDOMgross"]["amount"],
            reverse=True,
        )[0]
        self.biggest_domestic_openning_movie = sorted(
            self.directed_pics,
            key=lambda movie: movie["XDOMopenning"]["amount"],
            reverse=True,
        )[0]
        return [
            self.highest_grossing_worldwide_movie,
            self.highest_grossing_domestically_movie,
            self.biggest_domestic_openning_movie,
        ]

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, directed_pics):
        self._data = [
            (["Rank", "Movie", "Budget", "Domestic Gross", "Worldwide Gross"])
                      ,]
        for movie in enumerate(directed_pics, start=1):
            self._data.append([
                f'{movie[0]}',
                movie[1]["title"],
                f'${int(movie[1]["budget"]["amount"]):,}',
                f'${movie[1]["XDOMgross"]["amount"]:,}',
                f'${movie[1]["XWWgross"]["amount"]:,}'
            ])



def main():
    name = input("Director's fullname: ")
    director_info = get_director(name)
    director_info_first = director_info["d"][0]
    director_id = director_info_first["id"]
    director_name = director_info_first["l"]
    director_image = director_info_first["i"]

    # with open("director_image.txt", "w") as f:
    #     f.write(json.dumps(director_image))


    movies = get_movies(director_id)
    movies = movies["filmography"]
    directed_pics = []

    for movie in movies:
        try:
            if (
                movie["category"] == "director"
                and movie["status"] == "released"
                and movie["titleType"] == "movie"
            ):
                directed_pics.append(movie)
        except KeyError:
            pass

    directed_pics = get_box_office(directed_pics)
    # with open("directed_pics.txt", "w") as f:
    #     f.write(json.dumps(directed_pics))

    director_image = return_link_to_croped_image(
        "director_image_cropped.jpg", **director_image
    )

    pdf = make_pdf(director_name, director_image, directed_pics)
    os.makedirs("output PDF files/", exist_ok=True)
    pdf.output(f"output PDF files/{director_name}.pdf")

    clean_up_temp_files()


def make_pdf(director_name, director_image, directed_pics):
    pdf = PDF(
        director_name,
        director_image,
        directed_pics,
        orientation="P",
        unit="mm",
        format="A4",
    )

    ###Page 1
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Helvetica", "", 18)
    pdf.cell(0, 0, "Total Domestic Box Office: ", new_x=XPos.WCONT)
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 0, f"${pdf.total_DOM():,}", new_x=XPos.LMARGIN)
    pdf.ln(10)

    pdf.set_font("Helvetica", "", 18)
    pdf.cell(0, 0, "Total International Box Office: ", new_x=XPos.WCONT)
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 0, f"${pdf.total_NDOM():,}", new_x=XPos.LMARGIN)
    pdf.ln(10)

    pdf.set_font("Helvetica", "", 18)
    pdf.cell(0, 0, "Feature Films Released in Theaters:  ", new_x=XPos.WCONT)
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 0, f"{pdf.number_of_features}", new_x=XPos.LMARGIN)
    pdf.ln(10)

    top_movies = pdf.top_movies_getter()

    # print top movies
    cell_width = 50
    cell_height = 7
    poster_height = 75
    pdf.set_xy(12, 156)
    pdf.multi_cell(cell_width, cell_height, f"Highest Grossing Worldwide", align="C")
    pdf.image(pdf.highest_grossing_worldwide_movie["image"]["url"], 12, 180, cell_width, poster_height)
    pdf.set_xy(12, 263)
    pdf.cell(cell_width, 0, f"${pdf.highest_grossing_worldwide_movie['XWWgross']['amount']:,}", align="C")

    pdf.set_xy(78, 156)
    pdf.multi_cell(cell_width, cell_height, f"Highest Grossing Domestically", align="C")
    pdf.image(pdf.highest_grossing_domestically_movie["image"]["url"], 78, 180, cell_width, poster_height)
    pdf.set_xy(78, 263)
    pdf.cell(cell_width, 0, f"${pdf.highest_grossing_domestically_movie['XDOMgross']['amount']:,}", align="C")

    pdf.set_xy(144, 156)
    pdf.multi_cell(cell_width, cell_height, f"Biggest Domestic Openning", align="C")
    pdf.image(pdf.biggest_domestic_openning_movie["image"]["url"], 144, 180, cell_width, poster_height)
    pdf.set_xy(144,263)
    pdf.cell(cell_width, 0, f"${pdf.biggest_domestic_openning_movie['XDOMopenning']['amount']:,}", align="C")

    ###Pages 2 - onwards, print the table
    pdf.add_page()
    pdf.set_font('Helvetica', '', 14)
    with pdf.table(col_widths=(13, 30, 25, 30, 30)) as table:
        for data_row in pdf.data:
            row = table.row()
            for datum in data_row:
                row.cell(datum)

    ###Print data vis
    directed_pics = sort_by_year(directed_pics)
    if len(directed_pics) <= 12:
        x = [f'{movie["title"]}\n{movie["year"]}' for movie in directed_pics]
    if len(directed_pics) >= 13:
        x = [f'{movie["title"]}' for movie in directed_pics]
    y = [movie["XWWgross"]["amount"] / 10**6 for movie in directed_pics]
    z = [movie["XDOMgross"]["amount"] / 10**6 for movie in directed_pics]
    plt.plot(y)
    plt.plot(z)
    plt.legend(["Worldwide", "Domestic"])
    plt.xticks(range(len(x)), x)
    if len(directed_pics) >= 6 or any(len(_) > 27 for _ in x):
        plt.xticks(rotation=90)
    plt.title("Box Office Graph")
    plt.ylabel("Gross in $Millions")
    plt.tight_layout()
    plt.savefig("graph.png")

    pdf.image("graph.png", w=186)
    os.remove("graph.png")

    return pdf

def get_director(name):
    url = "https://online-movie-database.p.rapidapi.com/auto-complete"

    querystring = {"q": name}

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "online-movie-database.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers, params=querystring)
    return response.json()


def get_movies(id):
    url = "https://online-movie-database.p.rapidapi.com/actors/get-all-filmography"

    querystring = {"nconst": id}

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "online-movie-database.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers, params=querystring)
    return response.json()


def get_box_office(directed_pics):
    for movie in directed_pics:
        movie["id"] = extract_title(movie["id"])
        print(movie["title"])
        id = movie["id"]
        url = "https://online-movie-database.p.rapidapi.com/title/v2/get-business"

        querystring = {"tconst": id}

        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "online-movie-database.p.rapidapi.com",
        }

        response = requests.get(url, headers=headers, params=querystring)
        o = response.json()["titleBoxOffice"]

        if "budget" in o:
            movie["budget"] = o["budget"]
        else:
            movie["budget"] = {"amount": 0}


        try:
            movie["XWWgross"] = o["gross"]["aggregations"][0]["total"]
        except KeyError:
            movie["XWWgross"] = {"amount": 0}
        except TypeError:
            movie["XWWgross"] = {"amount": 0}

        try:
            movie["XDOMgross"] = o["gross"]["regional"][0]["total"]
        except KeyError:
            movie["XDOMgross"] = {"amount": 0}
        except TypeError:
            movie["XDOMgross"] = {"amount": 0}

        try:
            movie["XDOMopenning"] = o["openingWeekendGross"]["regional"][0]["total"]
        except KeyError:
            movie["XDOMopenning"] = {"amount": 0}
        except TypeError:
            movie["XDOMopenning"] = {"amount": 0}
    directed_pics = [
        movie for movie in directed_pics
        if (movie["XDOMgross"]["amount"] != 0 and movie["XWWgross"]["amount"]!= 0)
        ]
    return directed_pics


def extract_title(string):
    if matches := re.fullmatch(r"/title/(.*)/", string):
        return matches.group(1)
    return None

def return_link_to_croped_image(output_name, height, imageUrl, width):
    image = Image.open(save_and_pass_from_url(imageUrl, output_name))
    if image.size[1] < 1376:
        image = image.resize((1376*width//height, 1376), Image.Resampling.LANCZOS)
        width, height = image.size
    new_height, new_width = 975, 749
    left = (width - new_width) / 2
    top = (height - new_height) / 2 - 200
    right = (width + new_width) / 2
    bottom = (height + new_height) / 2 - 200

    image = image.crop((left, top, right, bottom))
    image.save(output_name)
    return output_name

def save_and_pass_from_url(imageUrl, output_name):
    urllib.request.urlretrieve(imageUrl, output_name)
    return output_name

def sort_by_year(list):
    return sorted(
            list, key=lambda movie: movie["year"], reverse=False
        )

def clean_up_temp_files():
    os.remove("director_image_cropped.jpg")

if __name__ == "__main__":
    main()