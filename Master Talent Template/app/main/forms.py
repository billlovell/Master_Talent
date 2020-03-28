from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length
from flask_babel import _, lazy_gettext as _l
from app.models import Employee, User
from flask import request

class SearchForm(FlaskForm):
    q = StringField(_l('Search'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)


class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_l('About me'),
                             validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Please use a different username.'))


class PostForm(FlaskForm):
    post = TextAreaField(_l('Say something'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

class EmpForm(FlaskForm):
    """
    Form for to add an employee
    """
    employeeid = StringField(_l('Employee ID', validators=[DataRequired()]))
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    ProductGroup = StringField('Product Group', validators=[DataRequired()])
    SectorRank = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Submit')

class EmpForm1(FlaskForm):
    """
    Form to edit an mployee
    """
    employeeid = StringField(_l('Employee ID', validators=[DataRequired()]))
    SectorRanknew = StringField('Secotor Rank Update', validators=[DataRequired()])
    Comments = StringField('Comments', validators=[DataRequired()])
    submit = SubmitField('Submit')