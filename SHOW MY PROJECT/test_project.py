from project import extract_title
from project import sort_by_year
from project import clean_up_temp_files
import pytest

def main():
    pass


def test_extract_title():
    assert extract_title("/title/tt0468569/") == "tt0468569"


def test_sort_by_year():
    directed_pics = get_directed_pics()
    directed_pics = sort_by_year(directed_pics)
    for movie in directed_pics:
        print(movie["year"])
    assert directed_pics[0]["year"] < directed_pics[-1]["year"]


def test_clean_up_temp_files():
    open("director_image_cropped.jpg","w").close()
    with pytest.raises(FileExistsError):
        open("director_image_cropped.jpg","x")
    clean_up_temp_files()
    with pytest.raises(FileNotFoundError):
        open("director_image_cropped.jpg","r")

























































def get_directed_pics():
    return [
        {
            "category": "director",
            "id": "tt9639470",
            "image": {
                "height": 1500,
                "id": "/title/tt9639470/images/rm3508989953",
                "url": "https://m.media-amazon.com/images/M/MV5BZjgwZDIwY2MtNGZlNy00NGRlLWFmNTgtOTBkZThjMDUwMGJhXkEyXkFqcGdeQXVyMTEyMjM2NDc2._V1_.jpg",
                "width": 1013,
            },
            "status": "released",
            "title": "Last Night in Soho",
            "titleType": "movie",
            "year": 2021,
            "budget": {"amount": 43000000.0, "currency": "USD"},
            "XWWgross": {"amount": 22957625, "currency": "USD"},
            "XDOMgross": {"amount": 10127625, "currency": "USD"},
            "XDOMopenning": {"amount": 4178460, "currency": "USD"},
        },
        {
            "category": "director",
            "id": "tt8610436",
            "image": {
                "height": 12000,
                "id": "/title/tt8610436/images/rm2905589249",
                "url": "https://m.media-amazon.com/images/M/MV5BNTA0YTE5M2MtZTc0Ny00ODViLWI2ZjItOTU3YzJmNzdhYjI3XkEyXkFqcGdeQXVyNTI4MzE4MDU@._V1_.jpg",
                "width": 8100,
            },
            "status": "released",
            "title": "The Sparks Brothers",
            "titleType": "movie",
            "year": 2021,
            "budget": {"amount": 0},
            "XWWgross": {"amount": 1249115, "currency": "USD"},
            "XDOMgross": {"amount": 648665, "currency": "USD"},
            "XDOMopenning": {"amount": 273530, "currency": "USD"},
        },
        {
            "category": "director",
            "id": "tt3890160",
            "image": {
                "height": 2048,
                "id": "/title/tt3890160/images/rm2955687168",
                "url": "https://m.media-amazon.com/images/M/MV5BMjM3MjQ1MzkxNl5BMl5BanBnXkFtZTgwODk1ODgyMjI@._V1_.jpg",
                "width": 1382,
            },
            "status": "released",
            "title": "Baby Driver",
            "titleType": "movie",
            "year": 2017,
            "budget": {"amount": 34000000, "currency": "USD"},
            "XWWgross": {"amount": 226945087, "currency": "USD"},
            "XDOMgross": {"amount": 107825862, "currency": "USD"},
            "XDOMopenning": {"amount": 20553320, "currency": "USD"},
        },
        {
            "category": "director",
            "id": "tt1213663",
            "image": {
                "height": 2048,
                "id": "/title/tt1213663/images/rm1898371072",
                "url": "https://m.media-amazon.com/images/M/MV5BNzA1MTk1MzY0OV5BMl5BanBnXkFtZTgwNjkzNTUwMDE@._V1_.jpg",
                "width": 1382,
            },
            "status": "released",
            "title": "The World's End",
            "titleType": "movie",
            "year": 2013,
            "budget": {"amount": 20000000, "currency": "USD"},
            "XWWgross": {"amount": 46091271, "currency": "USD"},
            "XDOMgross": {"amount": 26004851, "currency": "USD"},
            "XDOMopenning": {"amount": 8811790, "currency": "USD"},
        },
        {
            "category": "director",
            "id": "tt0446029",
            "image": {
                "height": 1600,
                "id": "/title/tt0446029/images/rm1060206848",
                "url": "https://m.media-amazon.com/images/M/MV5BNWI5ODc4MTAtN2U2NC00ZDk3LWE3NjAtNjIyODE2YTlhYjYwXkEyXkFqcGdeQXVyOTA3ODI3NDA@._V1_.jpg",
                "width": 1140,
            },
            "status": "released",
            "title": "Scott Pilgrim vs. the World",
            "titleType": "movie",
            "year": 2010,
            "budget": {"amount": 60000000, "currency": "USD"},
            "XWWgross": {"amount": 49421974, "currency": "USD"},
            "XDOMgross": {"amount": 33281690, "currency": "USD"},
            "XDOMopenning": {"amount": 10609795, "currency": "USD"},
        },
        {
            "category": "director",
            "freeTextAttributes": ['fake trailer segment "Don\'t"'],
            "id": "tt0462322",
            "image": {
                "height": 755,
                "id": "/title/tt0462322/images/rm2229441280",
                "url": "https://m.media-amazon.com/images/M/MV5BMjA0MzExNzc3MV5BMl5BanBnXkFtZTcwODAxMzM0MQ@@._V1_.jpg",
                "width": 496,
            },
            "status": "released",
            "title": "Grindhouse",
            "titleType": "movie",
            "year": 2007,
            "budget": {"amount": 67000000, "currency": "USD"},
            "XWWgross": {"amount": 25422088, "currency": "USD"},
            "XDOMgross": {"amount": 25037897, "currency": "USD"},
            "XDOMopenning": {"amount": 11596613, "currency": "USD"},
        },
        {
            "category": "director",
            "freeTextAttributes": ["directed by"],
            "id": "tt0425112",
            "image": {
                "height": 1486,
                "id": "/title/tt0425112/images/rm2797811200",
                "url": "https://m.media-amazon.com/images/M/MV5BMzg4MDJhMDMtYmJiMS00ZDZmLThmZWUtYTMwZDM1YTc5MWE2XkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg",
                "width": 1000,
            },
            "status": "released",
            "title": "Hot Fuzz",
            "titleType": "movie",
            "year": 2007,
            "budget": {"amount": 8000000.0, "currency": "GBP"},
            "XWWgross": {"amount": 80743363, "currency": "USD"},
            "XDOMgross": {"amount": 41210622, "currency": "USD"},
            "XDOMopenning": {"amount": 11536353, "currency": "USD"},
        },
        {
            "category": "director",
            "id": "tt0365748",
            "image": {
                "height": 1500,
                "id": "/title/tt0365748/images/rm4187183360",
                "url": "https://m.media-amazon.com/images/M/MV5BMTg5Mjk2NDMtZTk0Ny00YTQ0LWIzYWEtMWI5MGQ0Mjg1OTNkXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg",
                "width": 1004,
            },
            "status": "released",
            "title": "Shaun of the Dead",
            "titleType": "movie",
            "year": 2004,
            "budget": {"amount": 4000000.0, "currency": "GBP"},
            "XWWgross": {"amount": 38686535, "currency": "USD"},
            "XDOMgross": {"amount": 20959922, "currency": "USD"},
            "XDOMopenning": {"amount": 3300000, "currency": "USD"},
        },
    ]

if __name__ == "__main__":
    main()