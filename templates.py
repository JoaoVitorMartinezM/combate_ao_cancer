def replaces(data):
    # forms_copy = '''
    #             <div style="width: 300px;">
    #            <label >Nome Completo: </label>
    #            </div>
    #            <input type="text" value="full_name" disabled><br>
    #            <div style="width: 300px;">
    #            <label>Sexo: </label>
    #            </div>
    #            <input type="text" value="sex" disabled/><br>
    #            <div style="width: 300px;">
    #            <label>Data de Nascimento: </label>
    #            </div>
    #            <input type="text" value="age" disabled/><br>
    #            <div style="width: 300px;">
    #            <label>Comorbidades: </label>
    #            </div>
    #            <input type="text" value="has_disease" disabled/><br>
    #            <div style="width: 300px;">
    #            <label>Fuma: </label>
    #            </div>
    #            <input type="text" value="smoke" disabled/><br>
    #            <div style="width: 300px;">
    #            <label>Bebe: </label>
    #            </div>
    #            <input type="text" value="drink" disabled/><br>
    #            <div style="width: 300px;">
    #            <label>Tem câncer: </label>
    #            </div>
    #            <input type="text" value="have_cancer" disabled/><br>
    #            <div style="width: 300px;">
    #            <label>Histórico de câncer na família: </label>
    #            </div>
    #            <input type="text" value="history_of_cancer" disabled/><br>
    #            <div style="width: 300px;">
    #            <label>Foi ao dentista no último ano: </label>
    #            </div>
    #            <input type="text" value="went_dentist" disabled/><br>
    #            <div style="width: 300px;">
    #            <label>Consome chimarrão: </label>
    #            </div>
    #            <input type="text" value="consume_mate" disabled/><br>
    #            <div style="width: 300px;">
    #            <label>Usa protetor solar: </label>
    #            </div>
    #            <input type="text" value="sunscreen" disabled/><br>
    #            <div style="width: 300px;">
    #            <label>Teve insolação: </label>
    #            </div>
    #            <input type="text" value="sunstroke" disabled/><br>
    #            <div style="width: 300px;">
    #            <label>Tem lesão na pele: </label>
    #            </div>
    #            <input type="text" value="skin_lesion" disabled/><br>
    #
    #        '''
    # for key in data.keys():

        # key_ = key.split("-")
        # if data[key] and str(data[key]) == "True":
        #     forms_copy = forms_copy.replace(key_[0], "Sim")
        # elif not data[key] and str(data[key]) == "False":
        #     forms_copy = forms_copy.replace(key_[0], "Não")
        # else:
        #     forms_copy = forms_copy.replace(key_[0], str(data[key]))

    mail_template = '''
        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Template</title>
        </head>
        <style>
            body{
                gap: 20px;
                box-sizing: border-box;

            }
            .signature{

                width: 300px;
                height: 500px;
                border: 5px;
                border-radius:20px;

            }

        </style>
        <body>
            <h1>Recomendação de Avaliação de Saúde</h1>
            <h3>Boca: #mouth#%</h3>
            <h3>Pele: #skin#%</h3>

            <p>
                Após análise do seu questionário de saúde, sugerimos uma avaliação especializada de  #especialista#. Isso não indica necessariamente uma condição médica específica, mas é importante
                agendar uma consulta para uma avaliação aprofundada.
            </p>
            <p>
                
            </p>
            <img class="signature" style="border: 5px; width: 500px;" src="https://blog.oncosalud.pe/hs-fs/hubfs/cuidados%20para%20pacientes%20con%20cancer.jpg?width=3840&name=cuidados%20para%20pacientes%20con%20cancer.jpg">
            </img>
        </body>
        </html>
        '''
    mouth_score = data['mouth_score']
    skin_score = data['skin_score']
    mail_template = mail_template.replace("#mouth#", str(mouth_score))
    mail_template = mail_template.replace("#skin#", str(skin_score))

    if skin_score > 70 and mouth_score > 70:
        mail_template = mail_template.replace("#especialista#", "dermatologia e saúde bucal")
    elif skin_score > 70:
        mail_template = mail_template.replace("#especialista#", "dermatologia")
    else:
        mail_template = mail_template.replace("#especialista#", "saúde bucal")



    return mail_template
