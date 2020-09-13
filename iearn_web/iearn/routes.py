from datetime import datetime
import os, shutil
import secrets
from PIL import Image
from flask import (render_template, url_for, flash, redirect,
                    request, make_response, send_from_directory)
from iearn import app, db, bcrypt, ckeditor, mail
from iearn.forms import (LoginForm, UpdateAboutUsForm,
                     EditProjectForm, CreateTeamMemberForm, MediaContactsForm,
                      RequestResetForm, ResetPasswordForm)
from iearn.models import (Admin, AboutPost, ProjectPost, ArticleImages,
                     TemporaryImg, TeamMembers, Contacts, MediaLinks)
from flask_login import login_user, logout_user , current_user, login_required
from sqlalchemy import func
from flask_ckeditor import upload_success, upload_fail
from flask_mail import Message


#----------------  ROUTES  -----------------------------------------------------------------
#---------- COOKIES ------------------
@app.route("/cookies")
def cookies():

    resp = make_response("Cookies")

    resp.set_cookie(
        "flavor",
        value="chocolate chip"
    )

    return resp
#---- User authentication ---------
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
        
    # Laikinai sukuriamas Admin vartotojas
    if db.session.query(Admin).filter_by(email='just.kaulakis@gmail.com').count() < 1:
        hashed_admin_pw = bcrypt.generate_password_hash('slaptas').decode('utf-8')
        admin_reg = Admin(email='just.kaulakis@gmail.com', password=hashed_admin_pw)
        db.session.add(admin_reg)
        db.session.commit()

    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin and bcrypt.check_password_hash(admin.password, form.password.data):
            login_user(admin)
            return redirect(url_for('admin'))
        else:
            flash('Prisijungimas nesėkmingas. Prašome patikrinti laukelius', 'danger')
    return render_template('prisijungimas.html', title='Prisijungimas', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('veikla'))

#---- Not ADMIN ROUTES ---------

@app.route('/')
@app.route('/pagrindinis', methods=['GET', 'POST'])
def veikla():
    #image_file = url_for('static', filename="images/default_image.jpg")
    about = AboutPost.query.get(1)
    if about == None:
        about = AboutPost(content="-")
        db.session.add(about)
        db.session.commit()
    projects = ProjectPost.query.filter_by(is_posted=True)\
        .order_by(ProjectPost.date_posted.desc())
    projects = projects[0:4]
    club_members = TeamMembers.query.all()
    contacts = Contacts.query.all()
    links = MediaLinks.query.all()
    return render_template('veikla.html', projects=projects, about=about, contacts=contacts,
                            links=links, club_members=club_members)

@app.route('/projektai')
def projects():
    page = request.args.get('page', 1, type=int)
    published_projects = ProjectPost.query.filter_by(is_posted=True)\
        .order_by(ProjectPost.date_posted.desc())\
        .paginate(page=page, per_page=6)
    #published_projects = published_projects[::-1]
    return render_template('projektai.html', title='Projektai', published_projects=published_projects)

@app.route('/projektai/<int:project_id>')
def read_article(project_id):
    project = ProjectPost.query.get_or_404(project_id)
    if not project.is_posted:
        return "<h2>Forbidden Page</h2><p>403 Error</p>"
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['UPLOADED_PATH'] = os.path.join(basedir, 'static/images/article-images')
    return render_template('skaityti-projekta.html', title=project.title, project=project)


#---------------- ADMIN ROUTES  -----------------------------------------------------------------

def save_picture(form_picture, path_of_picture_folder, max_img_width):  # Išsaugoti nuotrauką į jam priskyrta failą failą
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', path_of_picture_folder, picture_fn) 
    
    img = Image.open(form_picture)
    # Read the images' width and height
    width, height = img.size

    # Resize the image keeping the aspect ratio if the max width is to big
    if width > max_img_width:
        wpercent = (max_img_width/float(width))
        hsize = int((float(height)*float(wpercent)))
        img = img.resize((max_img_width,hsize), Image.ANTIALIAS)
        
    img.save(picture_path)  # Save picture to a file
    
    return picture_fn, picture_path      # Return the name of image and the full path




@app.route('/admin/apie-mus', methods=['GET', 'POST'])
@login_required
def about_us():
    form = UpdateAboutUsForm()
    about = AboutPost.query.get(1)
    if form.validate_on_submit():
        about.content = form.content.data
        if form.picture.data:
            if about.image_path:
                os.remove(about.image_path)
            picture_file, picture_path = save_picture(form.picture.data, 'Apie_mus_nuotr', 935)
            about.image_file = picture_file
            about.image_path = picture_path
        db.session.commit()
        
        flash('Ši sekcija atnaujinta!', 'success')
        return redirect(url_for('about_us'))
    elif request.method == 'GET':
        form.content.data = about.content
    return  render_template('a-apie-mus.html', title='Apie mus', form=form, about=about)



@app.route('/admin')
@app.route('/admin/visi-projektai')
@login_required
def admin():
    posts = ProjectPost.query.all()
    return  render_template('a-visi-projektai.html', title='Visi projektai', posts=posts[::-1])

#------------------------------------------------------------CKEditor image upload managing-----------
@app.route('/admin/files/<path:filename>')
def uploaded_files(filename):
    path = app.config['UPLOADED_PATH'] # 1 is to images/temp, 
                                       # 2 is to images/article-images
    return send_from_directory(path, filename) # Load image from directory
                                                                                                  
@app.route('/admin/upload', methods=['POST'])
def upload():
    f = request.files.get('upload')
    # Add more validations here
    extension = f.filename.split('.')[-1].lower()
    if extension not in ['jpg', 'png', 'jpeg']:
        return upload_fail(message='Kelti tiktai nuotraukų tipo failus!')
    print(app.config['UPLOADED_PATH'])
    full_path = os.path.join(app.config['UPLOADED_PATH'], f.filename)
    f.save(full_path)
    head, tail = os.path.split(app.config['UPLOADED_PATH'])
    if tail == 'temp':
        image = TemporaryImg(image_file=f.filename, image_path=full_path)
    elif tail == 'article-images':
        image = ArticleImages(image_file=f.filename, image_path=full_path, article_id=app.config['THE_POST_ID'])
    
    db.session.add(image)
    db.session.commit()
    print("    Image inserted")
    print(TemporaryImg.query.all())
    print(ArticleImages.query.all())
    
    url = url_for('uploaded_files', filename=f.filename)
    return upload_success(url=url)  # return upload_success call
#-----------------------------------------------------------------------------------------

@app.route('/admin/visi-projektai/projekto-kurimas', methods=['GET', 'POST'])
@login_required
def create_project():
    print('page loaded')
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['UPLOADED_PATH'] = os.path.join(basedir, 'static/images/temp')
    folder = app.config['UPLOADED_PATH']

    print(TemporaryImg.query.all())
    print(ArticleImages.query.all())

    form = EditProjectForm()
    if form.validate_on_submit():
        print('    submitted')
        print(TemporaryImg.query.all())
        print(ArticleImages.query.all())
        old_folder = folder
        folder = app.config['UPLOADED_PATH'] = os.path.join(basedir, 'static/images/article-images')

        post = ProjectPost(title=form.title.data, description=form.short_description.data, article_body=form.body.data)
        db.session.add(post)
        db.session.commit()

        print('    folder length:  ' + str(len(os.listdir(old_folder))))
        if len(os.listdir(old_folder)) != 0:
            files_list = os.listdir(old_folder)
            for filename in files_list:
                #index = os.listdir(folder).index(filename)
                #print(index)
                temp = TemporaryImg.query.filter_by(image_file=filename).first()   # Move items from one db table to the other
                head, tail = os.path.split(temp.image_path)
                temp.image_path = os.path.join(folder, tail)
                article_image = ArticleImages(image_file=temp.image_file, image_path=temp.image_path, article_id=post.id)
                db.session.add(article_image)

                shutil.move(os.path.join(old_folder, filename), os.path.join(folder, filename)) # Move files from images/temp to images/article-images 
            db.session.commit()

        print('    Files transfered and stuff:')
        print(TemporaryImg.query.all())
        print(ArticleImages.query.all())

        if form.picture.data:
            thumbnail_file, thumbnail_path = save_picture(form.picture.data, 'Projektu nuotraukos', 256)
            post.thumbnail = thumbnail_file
            post.thumbnail_path = thumbnail_path
        if form.publish.data == True:
            post.is_posted = True
            post.date_posted = datetime.utcnow()
        db.session.add(post)
        db.session.commit()

        TemporaryImg.query.delete()         # Empty the temp images from db
        db.session.commit()
        print('    Deleted table:')
        print(TemporaryImg.query.all())
        for filename in os.listdir(old_folder): # Empty the images/temp folder
            file_path = os.path.join(old_folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
        
        return redirect(url_for('admin'))
    return  render_template('a-projekto-redagavimas.html', title='Projekto sukurimas', form=form)

@app.route('/admin/visi-projektai/redagavimas-<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_project(post_id):
    post = ProjectPost.query.get_or_404(post_id)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['UPLOADED_PATH'] = os.path.join(basedir, 'static/images/article-images')
    app.config['THE_POST_ID'] = post_id
    print(app.config['UPLOADED_PATH'])

    form = EditProjectForm()
    if form.validate_on_submit():
        if form.publish.data == True or form.save2.data == True:

            post.title = form.title.data
            post.description = form.short_description.data
            post.article_body=form.body.data

            if form.picture.data:
                if post.thumbnail_path:
                    os.remove(post.thumbnail_path)
                thumbnail_file, thumbnail_path = save_picture(form.picture.data, 'Projektu nuotraukos', 256)
                post.thumbnail = thumbnail_file
                post.thumbnail_path = thumbnail_path
            if form.publish.data == True:
                if post.date_posted == None:
                    post.date_posted = datetime.utcnow()
                post.is_posted = True
            db.session.commit()

            flash('Šis straipsnis atnaujintas!', 'success')
            return redirect(url_for('edit_project', post_id=post.id))
        if form.delete.data:
            
            for image in ArticleImages.query.filter_by(article_id=post.id).all(): # Delete images from db
                os.remove(image.image_path)
                db.session.delete(image)
            db.session.commit()
            
            db.session.delete(post)                                            # Delete whole article from db
            db.session.commit()
            return redirect(url_for('admin'))
    if request.method == 'GET':
        form.title.data = post.title
        form.short_description.data = post.description
        form.body.data = post.article_body

    return  render_template('a-projekto-redagavimas.html', title='Projekto redagavimas', form=form, post=post)

@app.route('/admin/komandos-nariai', methods=['GET', 'POST'])
@login_required
def team_members():
    members = TeamMembers.query.all()
    return  render_template('a-komandos-nariai.html', title='Komandos nariai', members=members)

@app.route('/admin/komandos-nariai/kurti-nari', methods=['GET', 'POST'])
@login_required
def create_member():
    form = CreateTeamMemberForm()
    if form.validate_on_submit():
        
        new_member = TeamMembers(name=form.name.data, description=form.member_description.data)
        db.session.add(new_member)
        db.session.commit()
        if form.profile_pic.data:
            profile_image_file, image_path = save_picture(form.profile_pic.data, 'Nariai', 240)
            new_member.profile_image_file = profile_image_file
            new_member.image_path = image_path
            print(new_member.profile_image_file)
        db.session.commit()
        
        #flash('Klubo narys sukurtas!', 'success')
        
        return redirect(url_for('team_members'))

    member = TeamMembers(name='', description='', profile_image_file='default-profile.jpg')
    return  render_template('a-nario-redagavimas.html', title='Nario sukurimas', form=form, member=member)

@app.route('/admin/komandos-nariai/redagavimas-<int:member_id>', methods=['GET', 'POST'])
@login_required
def edit_member(member_id):
    member = TeamMembers.query.get_or_404(member_id)

    form = CreateTeamMemberForm()
    if form.validate_on_submit():
        if form.save.data == True:
            member.name = form.name.data                        #  Change name of a member
            member.description = form.member_description.data   # Change description of a member

            if form.profile_pic.data:                           # If a picture is selected then change the profile
                if member.image_path != 'None':                 # picture of the member
                    os.remove(member.image_path)
                profile_image_file, image_path = save_picture(form.profile_pic.data, 'Nariai', 240)
                member.profile_image_file = profile_image_file
                member.image_path = image_path

            db.session.commit()

            flash('Klubo nartys atnaujintas!', 'success')
            return redirect(url_for('edit_member', member_id=member.id))
        elif form.delete.data == True:                         # If pressed "Delete", delete the member
            db.session.delete(member)
            db.session.commit()
            return redirect(url_for('team_members'))
    elif request.method == 'GET':                              #  When the page is loaded
        form.name.data = member.name                           #  show all of the member data in the inputs
        form.member_description.data = member.description
    return  render_template('a-nario-redagavimas.html', title='Nario redagavimas', form=form, member=member)

@app.route('/admin/media-kontaktai', methods=['GET', 'POST'])
@login_required
def media_contacts():
    form = MediaContactsForm()

    if form.validate_on_submit():
        for i in range(1,5):
            Contacts.query.get(i).content = form['contact' + str(i)].data
            db.session.add(Contacts.query.get(i))
            MediaLinks.query.get(i).web_link = form['Link' + str(i)].data
            db.session.add(MediaLinks.query.get(i))

        db.session.commit()
        for link in MediaLinks.query.all():
            print(link.web_name)
        flash('Informacija atnaujinta!', 'success')
        return redirect(url_for('media_contacts'))
    elif request.method == 'GET':
        if Contacts.query.all() == [] and MediaLinks.query.all() == []:
            web_names = ['Instagram', 'Facebook', 'YouTube', 'iEARN']
            for i in range(0,4):
                contact = Contacts(content='-')
                media_link = MediaLinks(web_name=web_names[i], web_link='#')
                db.session.add(contact)
                db.session.add(media_link)
                db.session.commit()
        else:
            for i in range(1, 5):
                form['contact' + str(i)].data = Contacts.query.get(i).content
                form['Link' + str(i)].data = MediaLinks.query.get(i).web_link
    contacts = Contacts.query.all()
    links = MediaLinks.query.all()
    return  render_template('a-media-kontaktai.html', title='Media ir kontaktai', form=form, contacts=contacts, links=links)

@app.route('/admin/mano-info', methods=['GET', 'POST'])
@login_required
def my_info():

    return  render_template('a-mano-info.html', title='Mano info')

# ---- RESET PASSWORD ----
def send_reset_email(admin):
    token = admin.get_reset_token()
    msg = Message('Slaptažodžio pakeitimo prašymas',
                  sender='djgytis231@gmail.com',
                  recipients=[admin.email])
    msg.body = f'''Norint pakeisti slaptažodį, paspauskite ant nurodytos nuorodos:
{url_for('reset_token', token=token, _external=True)}

Jeigu jūs neprašėte pakeisti slaptažodžio, tuomet ignoruokite šią žinutę ir jokių pakeitimų nebus padaryta.
'''
    mail.send(msg)


@app.route("/pakeisti-slaptazodi", methods=['GET', 'POST'])
def reset_request():    # Route where user is putting in an email to which to send instructions
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    form = RequestResetForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        send_reset_email(admin)
        flash('Į jūsų el. paštą buvo nusiųstos instrukcijos kaip pasikeisti slaptažodį.', 'info')
        return redirect(url_for('login'))
    return render_template('siusti-slpt-pakeitimo-prasyma.html', title='Pakeisti slaptažodį', form=form)


@app.route("/pakeisti-slaptazodi/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    admin = Admin.verify_reset_token(token)
    if admin is None:
        flash('Raktinis kodas nebegalioja arba jis nėra teisingas', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        admin.password = hashed_password
        db.session.commit()
        flash('Jųsū slaptažodis pakeistas! Galite prisijungti', 'success')
        return redirect(url_for('login'))
    return render_template('pakeisti-slaptazodi.html', title='Pakeisti slaptažodį', form=form)
