from django import forms
from django.shortcuts import render, redirect
from .forms import ImagesForm
from .models import Images
from django.http import JsonResponse
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView
from django.urls import reverse_lazy

@csrf_exempt
def index(request):
    error = ''

    images = Images.objects.filter()

    form = ImagesForm()

    data = {
        'form': form,
        'error': error,
        'images': images,
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.method == 'POST':

            idnft = str(request.body).split("'")[1]
            images_to_idnft = Images.objects.get(id_nft = idnft).description
            images_idnft_to_idnft = Images.objects.get(id_nft = idnft).id_nft

            dat = [images_to_idnft, images_idnft_to_idnft]

            return JsonResponse(dat, safe = False)


        # if request.method == 'POST-DB':
        #     for i in range(2001, 20001):
        #         Images.objects.create(id_nft = i, image = 'images/green.png', description = '')

    if request.method == 'POST':
        form = ImagesForm(request.POST, request.FILES)
        # print(form.data["image"])
        id_json = int(form.data["id_nft"])
        # description_json = form.data["description"]
        # image_json = form.data["image"]

        # image_post = Images.objects.filter(id_nft = id_json)
        # image_post.update(description = description_json)


        old_image = Images.objects.get(id_nft = id_json)
        form2 = ImagesForm(request.POST, request.FILES, instance=old_image)

        if form2.is_valid():
            form2.save()

        # image_post.update(image = image_json)
        # form.data._mutable = True
        # # form.data["id_nft"] = '1'
        # # form.data["id_owner"] = request.user.id
        # form.data._mutable = False
        # if form.is_valid():
        #     form.save()
        #     return redirect('main')
        # else:
        #     error = 'Форма была неверной'


        # if request.method == 'POST-SAVEDB':
            # my_bytes_value = request.body
            # my_json = my_bytes_value.decode('utf8').replace("'", '"')
            #
            # data = json.loads(my_json)
            # id_json = int(data['id'])
            # description_json = data['description']
            # image_json = data['getImg']
            #
            # image_post = Images.objects.filter(id_nft = id_json)
            # image_post.update(description = description_json)
            # image_post.update(image = image_json)



    return render(request, 'main/index.html', data)

class indexUpdateView(UpdateView):
    model = Images
    form_class = ImagesForm
    template_name = 'main/index.html'
    success_url = reverse_lazy('')
    context_object_name = 'index'
