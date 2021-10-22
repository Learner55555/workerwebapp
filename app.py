import io
import xlwt
from flask import Flask, jsonify, render_template, request, redirect, Response, session, url_for
from models import app, db, Workers
from urllib.parse import urlencode
db.init_app(app)

app.config.from_object('config')
import sys
import os
from forms import *



#  ----------------------------------------------------------------


# @app.route('/')
# def greeting():
#   return "Hello world! The app is actually working!"



#  ----------------------------------------------------------------

@app.route('/')
def logout():
  return redirect(url_for('get_workers'))
# #  ----------------------------------------------------------------


#  ----------------------------------------------------------------

@app.route('/workers', methods=['GET'])
def get_workers():
  all_workers = [i.format() for i in Workers.query.all()]
  return render_template('workers_page.html', workers=all_workers);

# ------------------------------------------------------------------

# @app.route('/workers/add', methods=['POST'])
# def edit_worker():
#   worker = Workers.query.filter_by(id=workers_id).first_or_404()
#   form = WorkerForm(obj=worker)
#   return render_template('edit_worker.html', form=form, worker=worker)


@app.route('/workers/create', methods=['GET'])
def create_worker_form():
  form = WorkerForm()
  return render_template('new_worker.html', form=form)

#  ----------------------------------------------------------------
# @app.route('/workers', methods=['POST'])
# def post_workers():
#       body = request.get_json()
#       worker_name = body.get('name', None)
#       worker_surname = body.get('surname', None)
#       worker_birth_date = body.get('birth_date', None)
#       worker_information = Workers(name = worker_name, surname=worker_surname, birth_date=worker_birth_date)
#       db.session.add(worker_information)
#       db.session.commit()
#       return redirect(url_for('get_workers')


@app.route('/workers/create', methods=['POST'])
def create_worker():
  form=WorkerForm(request.form)
  try:
        worker = Workers(
        name = form.name.data,
        surname = form.surname.data,
        birth_date = form.birth_date.data,
        )
        db.session.add(worker)
  except:
    print(sys.exc_info())
    db.session.rollback()
  finally:
    db.session.commit()
    db.session.close()
  return redirect(url_for('get_workers'))
  # except:
  #   error = True
  # finally:
  #   if error:
  #         db.session.rollback()
  #         db.session.close()
  #   else:
  #         db.session.commit()
  #         db.session.close()

  # except:
  #   db.session.rollback()
  # finally:
  #   db.session.close()
  # return redirect(url_for('get_workers')
  # # return render_template('pages/home.html')

#  ----------------------------------------------------------------

#  ----------------------------------------------------------------

@app.route('/delete/<int:workers_id>', methods=['DELETE', 'GET'])
def delete_actor(workers_id):
  deleting_worker = Workers.query.filter_by(id=workers_id).one_or_none()
  try:
    db.session.delete(deleting_worker)
    db.session.commit()
    return redirect('/workers')
  except:
    return "There was an error in deleting information"

@app.route('/export_to_excel/')
def download():
      all_information = Workers.query.all()
      # output in bytes
      output  = io.BytesIO()
      # create Workbook object
      workbook = xlwt.Workbook()
      # add a sheet
      sheet = workbook.add_sheet('Workers information')

      # add  headers
      sheet.write(0,0, 'Id')
      sheet.write(0,1, 'Name')
      sheet.write(0,2, 'Surname')
      sheet.write(0,3, 'Birth date')

      i=0
      for row in all_information:
            sheet.write(i+1, 0, str(row.id))
            sheet.write(i+1, 1, row.name)
            sheet.write(i+1, 2, row.surname)
            sheet.write(i+1, 3, str(row.birth_date))
            i+=1
      workbook.save(output)
      output.seek(0)

      return Response(output, mimetype = "application/ms-excel", headers = {"Content-Disposition":"attachment;filename=workers_information.xls"})



#----------------------------------------------------------------------------#


@app.route('/workers/<int:workers_id>/edit', methods=['GET'])
def edit_worker(workers_id):
  worker = Workers.query.filter_by(id=workers_id).first_or_404()
  form = WorkerForm(obj=worker)
  return render_template('edit_worker.html', form=form, worker=worker)

#----------------------------------------------------------------------------#

@app.route('/workers/<int:workers_id>/edit', methods=['POST'])
def edit_workers_submission(workers_id):
  worker = Workers.query.first_or_404(workers_id)
  form = WorkerForm(request.form)
  try:
    worker.name = form.name.data
    worker.surname = form.surname.data
    worker.birth_date = form.birth_date.data
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('get_workers', workers_id=workers_id))
