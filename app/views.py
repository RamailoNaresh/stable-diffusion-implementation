import os
from django.http import JsonResponse
import requests
from django.shortcuts import render
from rest_framework.decorators import api_view
import base64
from django.conf import settings


@api_view(["POST"])
def generate_image(request):
    try:
        engine_id = "stable-diffusion-v1-6"
        api_host = 'https://api.stability.ai'
        api_key = settings.API_KEY
        data = request.data
        if api_key is None:
            raise Exception("Missing Stability API key.")

        response = requests.post(
            f"{api_host}/v1/generation/{engine_id}/text-to-image",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            json={
                "text_prompts": [
                    {
                        "text": data.get('text')
                    }
                ],
                "cfg_scale": 7,
                "height": 1024,
                "width": 1024,
                "samples": 1,
                "steps": 30,
            },
        )

        if response.status_code != 200:
            raise Exception("Non-200 response: " + str(response.text))

        data = response.json()

        for i, image in enumerate(data["artifacts"]):
            with open(f"/home/mango/api_v1_txt2img_{i}.png", "wb") as f:
                f.write(base64.b64decode(image["base64"]))
        return JsonResponse({'message': "Image generated successfully"})
    except Exception as e:
        return JsonResponse({'message': str(e)})


@api_view(["POST"])
def upscale_image(request):
    try:
        engine_id = "esrgan-v1-x2plus"
        api_host = 'https://api.stability.ai'
        api_key = settings.API_KEY
        image = request.FILES.get('image')
        if api_key is None:
            raise Exception("Missing Stability API key.")

        response = requests.post(
            f"{api_host}/v1/generation/{engine_id}/image-to-image/upscale",
            headers={
                "Accept": "image/png",
                "Authorization": f"Bearer {api_key}"
            },
            files={
                "image": image.read()
            },
            data={
                "width": 1024,
            }
        )

        if response.status_code != 200:
            raise Exception("Non-200 response: " + str(response.text))

        with open(f"/home/mango/api_v1_upscaled_image.png", "wb") as f:
            f.write(response.content)
        return JsonResponse({'message': "Image generated successfully"})
    except Exception as e:
        return JsonResponse({'message': str(e)})


@api_view(["POST"])
def edit_image_remove_bg(request):
    try:
        api_key = settings.API_KEY
        data = request.FILES.get('image')
        response = requests.post(
            f"https://api.stability.ai/v2beta/stable-image/edit/remove-background",
            headers={
                "authorization": f"Bearer {api_key}",
                "accept": "image/*"
            },
            files={
                "image": data.read()
            },
            data={
                "output_format": "webp"
            },
        )

        if response.status_code == 200:
            with open("/home/mango/api_v1_edit_image.png", 'wb') as file:
                file.write(response.content)
        else:
            raise Exception(str(response.json()))
        return JsonResponse({'message': "Image generated successfully"})
    except Exception as e:
        return JsonResponse({'message': str(e)})


@api_view(["POST"])
def sketch_image(request):
    try:
        image = request.FILES.get('image')
        text = request.POST.get('text')
        api_key = settings.API_KEY
        response = requests.post(
            f"https://api.stability.ai/v2beta/stable-image/control/sketch",
            headers={
                "authorization": f"Bearer {api_key}",
                "accept": "image/*"
            },
            files={
                "image": image.read()
            },
            data={
                "prompt": text,
                "control_strength": 0.7,
                "output_format": "webp"
            },
        )

        if response.status_code == 200:
            with open("/home/mango/api_sketch.webp", 'wb') as file:
                file.write(response.content)
        else:
            raise Exception(str(response.json()))
        return JsonResponse({'message': "Image generated successfully"})
    except Exception as e:
        return JsonResponse({'message': str(e)})


def outpaint_image():
    api_key = settings.API_KEY
    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/edit/outpaint",
        headers={
            "authorization": f"Bearer {api_key}",
            "accept": "image/*"
        },
        files={
            "image": open("/home/mango/Downloads/naresh.jpg", "rb")
        },
        data={
            "left": 200,
            "down": 200,
            "output_format": "webp"
        },
    )

    if response.status_code == 200:
        with open("/home/mango/outpaint.webp", 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(str(response.json()))


def search_and_replace():
    api_key = settings.API_KEY
    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/edit/search-and-replace",
        headers={
            "authorization": f"Bearer {api_key}",
            "accept": "image/*"
        },
        files={
            "image": open("/home/mango/Downloads/naresh.jpg", "rb")
        },
        data={
            "prompt": "god shiva snake ",
            "search_prompt": "muffler"
        }
    )

    if response.status_code == 200:
        with open("/home/mango/replace.webp", 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(str(response.json()))


def inpaint():
    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/edit/inpaint",
        headers={
            "authorization": f"Bearer sk-MYAPIKEY",
            "accept": "image/*"
        },
        files={
            "image": open("/home/mango/Downloads/naresh.jpg", "rb")
        },
        data={
            "prompt": "replace cloth with party suit",
            "output_format": "webp",
        },
    )

    if response.status_code == 200:
        with open("./dog-wearing-black-glasses.webp", 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(str(response.json()))
