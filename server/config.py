# from classes.property_details import ExtractPropertyDetails
# from classes.property_groups import ExtractPropertyGroups
from flask import Flask, session, request, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin as SM
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import validates
# from classes.pdf_handling import PdfDataExtractor
# from classes.scraping import ScrapeSite
from flask_cors import CORS
# from models.property import Property
import os

db = SQLAlchemy()