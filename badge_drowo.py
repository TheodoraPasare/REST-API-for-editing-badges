import csv
import os
from PIL import Image, ImageDraw, ImageFont


def read_names_from_csv(filename):
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        names = []
        for row in reader:
            if len(row) >= 2:
                first_names = " ".join(row[:-1])  # Toate elementele mai puțin ultimul sunt prenume
                last_name = row[-1]  # Ultimul element este numele de familie
                names.append((first_names, last_name))
    return names


def generate_badge(template_path, output_path, first_name, last_name):
    image = Image.open(template_path)
    draw = ImageDraw.Draw(image)
    max_width, max_height = 520, 170  # Dimensiunea maximă permisă pentru un rând
    font_size = 150  # Dimensiune inițială mare

    font_path = "GeorgiaPro-Black.ttf"  # Asigură-te că fișierul .ttf este în același folder cu scriptul

    while font_size > 10:
        font = ImageFont.truetype(font_path, font_size)
        text = f"{first_name} {last_name}"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Dacă textul încape, ne oprim
        if text_width <= max_width and text_height <= max_height:
            break
        font_size -= 2

    # Dacă fontul este prea mic, împărțim numele pe două rânduri
    if font_size <= 50:
        font_size = 80  # Resetăm fontul la o dimensiune mai mare pentru două rânduri
        font = ImageFont.truetype(font_path, font_size)

        full_name = f"{first_name} {last_name}"
        words = full_name.split()
        half = len(words) // 2
        line1 = " ".join(words[:half])
        line2 = " ".join(words[half:])

        # Ajustăm fontul pentru fiecare linie în parte astfel încât să încapă în max_width
        while font_size > 10:
            # Calculăm dimensiunile pentru fiecare linie
            bbox1 = draw.textbbox((0, 0), line1, font=font)
            bbox2 = draw.textbbox((0, 0), line2, font=font)
            text_width1 = bbox1[2] - bbox1[0]
            text_width2 = bbox2[2] - bbox2[0]

            # Dacă ambele linii încape în lățimea maximă, ne oprim
            if text_width1 <= max_width and text_width2 <= max_width:
                break
            font_size -= 2  # Dacă nu încap, micșorăm fontul

            # Actualizăm fontul la dimensiunea nouă
            font = ImageFont.truetype(font_path, font_size)

        # Calculăm dimensiunile pentru fiecare linie cu fontul ajustat
        bbox1 = draw.textbbox((0, 0), line1, font=font)
        bbox2 = draw.textbbox((0, 0), line2, font=font)
        text_width1 = bbox1[2] - bbox1[0]
        text_width2 = bbox2[2] - bbox2[0]

        # Calculăm pozițiile pentru centrare
        pos_x1 = 245 + (max_width - text_width1) // 2
        pos_x2 = 245 + (max_width - text_width2) // 2

        # Poziționăm rândurile corect pe badge
        pos_y1 = 475
        pos_y2 = 525 

        # Verificăm dimensiunile și ajustăm distanța dintre rânduri
        line_height = bbox1[3] - bbox1[1] + 10  # Adăugăm spațiu între linii
        pos_y2 = pos_y1 + line_height  # Calculăm poziția pentru al doilea rând

        draw.text((pos_x1, pos_y1), line1, fill="white", font=font)
        draw.text((pos_x2, pos_y2), line2, fill="white", font=font)

    else:
        # Scriem numele normal pe un singur rând
        text_position = (245, 515)
        draw.text(text_position, text, fill="white", font=font)

    image.save(f"{output_path}/{first_name.replace(' ', '_')}_{last_name}.png")


def process_badges(csv_filename, template_path, output_path):
    os.makedirs(output_path, exist_ok=True)  # Creează folderul dacă nu există
    names = read_names_from_csv(csv_filename)
    for first_name, last_name in names:
        generate_badge(template_path, output_path, first_name, last_name)



csv_filename1 = "logistic_csv.txt"
template_path1 = "logistic_nou.png"
output_path1 = "badges_logistic"
process_badges(csv_filename1, template_path1, output_path1)


csv_filename2 = "participanti_csv.txt"
template_path2 = "participant_nou.png"
output_path2 = "badges_participanti"
process_badges(csv_filename2, template_path2, output_path2)


csv_filename3 = "traineri_csv.csv"
template_path3 = "trainer_nou.png"
output_path3 = "badges_traineri"
process_badges(csv_filename3, template_path3, output_path3)
