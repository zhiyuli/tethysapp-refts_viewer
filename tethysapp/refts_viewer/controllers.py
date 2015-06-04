from django.shortcuts import render
from utilities import *
from django.http import Http404

#Base_Url_HydroShare REST API
#url_base='http://{0}.hydroshare.org/hsapi/resource/{1}/files/{2}'
#url_base='http://{0}.hydroshare.org/django_irods/download/?path={1}/{2}'
url_base='http://{0}.hydroshare.org/django_irods/download/{1}/data/contents/{2}'

##Call in Rest style
def restcall(request,branch,res_id,filename):
    try:
        print "restcall", branch, res_id, filename
        url_wml = url_base.format(branch, res_id, filename)

        response = urllib2.urlopen(url_wml)

        html = response.read()

        timeseries_plot = chartPara(html, filename)

        context = {"timeseries_plot": timeseries_plot}
    except:
        raise Http404("Cannot locate this resource file")

    return render(request, 'refts_viewer/home.html', context)

#Normal Get or Post Request
#http://dev.hydroshare.org/hsapi/resource/72b1d67d415b4d949293b1e46d02367d/files/referencetimeseries-2_23_2015-wml_2_0.wml/
def home(request):
    try:
        filename=None
        res_id=None
        url_wml=None
        branch=None

        if request.method == 'POST' and 'res_id' in request.POST and 'filename' in request.POST:
           #print request.POST
           filename = request.POST['filename']
           res_id=  request.POST['res_id']
           branch= request.POST['branch']
           url_wml= url_base.format(branch,res_id,filename)
        elif request.method == 'GET' and 'res_id' in request.GET and 'filename' in request.GET:
            #print request.GET
            filename = request.GET['filename']
            res_id = request.GET['res_id']
            branch= request.GET['branch']
            url_wml= url_base.format(branch,res_id,filename)
        elif request.method == 'GET' and 'res_id' in request.GET and 'fileurl' in request.GET:
            res_id = request.GET['res_id']
            url_wml = request.GET['fileurl']


        if url_wml is None:
            filename = 'KiWIS-WML2-Example.wml'
            url_wml='http://www.waterml2.org/KiWIS-WML2-Example.wml'

        print "HS_REST_API: " + url_wml

        response = urllib2.urlopen(url_wml)

        print ("Start to download")
        html = response.read()
        print ("Download completed")

        timeseries_plot = chartPara(html,filename)


        context = {"timeseries_plot": timeseries_plot}
    except:
        raise Http404("Cannot locate this resource file!")
    return render(request, 'refts_viewer/home.html', context)


def request_demo(request):

    name = ''

    # Define Gizmo Options
    text_input_options_res_id = {'display_text': 'HydroShare Resource ID',
                          'name': 'res_id',
                            'initial': 'c377d07efcfb484ab0da1c5c2ec7c7ac'}

    text_input_options_filename = {'display_text': 'Resource Filename (WaterML2.0)',
                          'name': 'filename',
                          'initial': 'refts1-wml_2_0.xml'
                          }


    # Create template context dictionary
    context = {'name': name,
               'text_input_options_res_id': text_input_options_res_id,
               'text_input_options_filename':text_input_options_filename
               }

    return render(request, 'refts_viewer/request_demo.html',context)
