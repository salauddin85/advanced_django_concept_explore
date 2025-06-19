from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.template import Template, Context
from django.core.mail import EmailMultiAlternatives

from .models import EmailCompose

class SendEmailView(APIView):
     def post(self, request):
        try:
            compose_id = request.data.get("compose_id")
            email_data_list = request.data.get("data", [])

            if not compose_id or not email_data_list:
                return Response({"error": "compose_id and data are required"}, status=400)

            compose = EmailCompose.objects.get(id=compose_id)
            template = Template(compose.body)

            for item in email_data_list:
                user_email = item.get("email")
                context_data = item.get("context", {})

                if not user_email:
                    continue  # skip if email missing

                # render template with individual context
                context = Context(context_data)
                rendered_html = template.render(context)

                email = EmailMultiAlternatives(
                    subject=compose.subject,
                    body=rendered_html,
                    from_email="ahmedsalauddin677785@gmail.com",
                    to=[user_email]
                )
                email.attach_alternative(rendered_html, "text/html")
                email.send()

            return Response({"message": "Emails sent successfully ✅"}, status=status.HTTP_200_OK)

        except EmailCompose.DoesNotExist:
            return Response({"error": "EmailCompose object not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)