import sqlite3

# Connect to SQLite database (creates a new database if not exists)
conn = sqlite3.connect('myDB.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Define SQL queries
movie_query = '''

    INSERT INTO movie VALUES
    (1, "Matrix", "Lana Wachowski", 136, "Keanu Reeves, Christina Ricci, Carrie-Anne Moss",
    "When a beautiful stranger leads computer hacker Neo to a forbidding underworld, he discovers the shocking truth: the life he knows is the elaborate deception of an evil cyber-intelligence.",
    "https://cdn.shopify.com/s/files/1/0057/3728/3618/products/ed4796ac6feff9d2a6115406f964c928_6b200bda-fe71-4900-ad7f-903cdda50dab_480x.progressive.jpg?v=1573587596"),

    (2, "Pulp Fiction", "Quentin Tarantino", 154, "John Travolta, Uma Thurman, Samuel L. Jackson",
    "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
    "https://cdn.shopify.com/s/files/1/0057/3728/3618/products/950e439404c3d5eddd86ae876cec83bf_949b5045-2503-4883-bcd2-ff1f31f5b14c_480x.progressive.jpg?v=1573588746"),

    (3, "Forrest Gump", "Robert Zemeckis", 182, "Tom Hanks, Robin Wright, Gary Sinise",
    "The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal and other historical events unfold from the perspective of an Alabama man with an IQ of 75, whose only desire is to be reunited with his childhood sweeth.",
    "https://cdn.shopify.com/s/files/1/0057/3728/3618/products/03c89d6a4c0565f265ccff5c4033e8d2_480x.progressive.jpg?v=1573615828"),

    (4, "Dune", "Denis Villeneuve", 195, "Timothée Chalamet, Rebecca Ferguson, Zendaya",
    "Feature adaptation of Frank Herbert's science fiction novel, about the son of a noble family entrusted with the protection of the most valuable asset and most vital element in the galaxy.",
    "https://cdn.shopify.com/s/files/1/0057/3728/3618/products/dune_tfc43wep_480x.progressive.jpg?v=1634918156"),

    (5, "Spencer", "Pablo Larraín", 111, "Kristen Stewart, Timothy Spall, Jack Nielen",
    "During her Christmas holidays with the royal family at the Sandringham estate in Norfolk, England, Diana Spencer, struggling with mental health problems, decides to end her decade-long marriage to Prince Charles.",
    "https://cdn.shopify.com/s/files/1/0057/3728/3618/products/spencer_sbxxrd3u_480x.progressive.jpg?v=1635440026"),

    (6, "Last Night in Soho", "Edgar Wright", 116, "Thomasin McKenzie, Anya Taylor-Joy, Matt Smith",
    "An aspiring fashion designer is mysteriously able to enter the 1960s where she encounters a dazzling wannabe singer. But the glamour is not all it appears to be and the dreams of the past start to crack and splinter into something dangerous.",
    "https://cdn.shopify.com/s/files/1/0057/3728/3618/products/last_night_in_soho_ver2_480x.progressive.jpg?v=1633027853"),

    (7, "Joker","Todd Phillips",122,"Joaquin Phoenix, Robert De Niro, Zazie Beetz",
    "In Gotham City, mentally troubled comedian Arthur Fleck is disregarded and mistreated by society. He then embarks on a downward spiral of revolution and bloody crime. This path brings him face-to-face with his alter-ego: the Joker.",
    "https://cdn.shopify.com/s/files/1/0057/3728/3618/products/JOKER.PW.REP_480x.progressive.jpg?v=1574965207");
'''

screen_query = '''
    INSERT INTO screen VALUES
    (1, "Hall 1", 30),
    (2, "Hall 2", 15),
    (3, "Hall 3", 40);
'''

projection_query = '''

    INSERT INTO projection VALUES

    (999, '2024-02-09', '12:00:00', 1, 3);
'''

# Execute the queries
#cursor.executescript(movie_query)
#cursor.executescript(screen_query)
cursor.executescript(projection_query)

# Commit changes and close the connection
conn.commit()
conn.close()

print("SQL queries executed successfully.")
