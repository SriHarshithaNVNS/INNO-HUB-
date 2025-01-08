import mysql.connector

# Connect to MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123",
    database="innovator"
)
cursor = connection.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS uploads (
    id INT,           
    uid INT AUTO_INCREMENT PRIMARY KEY,
    pname VARCHAR(100) NOT NULL,
    cat VARCHAR(100) NOT NULL,
    des VARCHAR(500) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    video_data LONGBLOB
);
                
""")

# # Upload file to database
# def upload_file(file_path):
#     with open(file_path, "rb") as file:
#         file_data = file.read()
#         file_name = file.name

#     query = "INSERT INTO files (name, data) VALUES (%s, %s)"
#     cursor.execute(query, (file_name, file_data))
#     connection.commit()

# # # Download file from database
# # def download_file(file_id):
# #     query = "SELECT name, data FROM files WHERE id = %s"
# #     cursor.execute(query, (file_id,))
# #     file_data = cursor.fetchone()

# #     if file_data:
# #         file_name, file_content = file_data
# #         with open(file_name, "wb") as file:
# #             file.write(file_content)
# #         print("File uploaded successfully")    
# #     else:
# #         print("File not found")


# import PyPDF2
# import unicodedata

# def download_file(file_id):
#     query = "SELECT name, data FROM files WHERE id = %s"
#     cursor.execute(query, (file_id,))
#     file_data = cursor.fetchone()

#     if file_data:
#         file_name, file_content = file_data
#         with open(file_name, "wb") as file:
#             file.write(file_content)
#             print(f"File '{file_name}' downloaded successfully")

#         # Open the downloaded PDF file and extract text
#         with open(file_name, "rb") as pdf_file:
#             pdf_reader = PyPDF2.PdfReader(pdf_file)

#             text = ""
#             for page in pdf_reader.pages:  # Iterate directly over pages
#                 text += page.extract_text()

#             print("Text extracted from PDF:")
#             normalized_text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
#             print(normalized_text)
#     else:
#         print("File not found")        


# # Example usage
# upload_file(r"D:\Inno_Hub\innovator\test\1.pdf")
# download_file(9)

# Close MySQL connection
cursor.close()
connection.close()


