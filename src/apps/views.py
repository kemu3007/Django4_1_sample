import asyncio
import time
from logging import getLogger

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.http import HttpResponse
from django.views import View
from model_bakery import baker

logger = getLogger(__name__)


class AsyncView(View):
    async def get(self, request, *args, **kwargs):
        # Perform view logic using await.
        await asyncio.sleep(1)
        return HttpResponse("Hello World")


def bulk_create(process: str, model, instances):
    start = time.time()
    print(f"sync start_agg {process}")
    model.objects.bulk_create(instances)
    print(f"sync   end_agg {process} {time.time() - start}")


class SyncGetView(View):
    def get(self, request, *args, **kwargs):
        users = baker.prepare(User, _quantity=3000)
        sessions = baker.prepare(Session, _quantity=3000)
        start = time.time()
        bulk_create("user", User, users)
        bulk_create("session", Session, sessions)
        end = time.time()
        return HttpResponse(f"{end - start}")


async def abulk_create(process: str, model, instances):
    start = time.time()
    print(f"async start_agg {process}")
    await model.objects.abulk_create(instances)
    print(f"async   end_agg {process} {time.time() - start}")


class AsyncGetView(View):
    async def get(self, request, *args, **kwargs):
        users = baker.prepare(User, _quantity=1000)
        sessions = baker.prepare(Session, _quantity=1000)
        start = time.time()
        await asyncio.gather(abulk_create("user", User, users), abulk_create("session", Session, sessions))
        end = time.time()
        return HttpResponse(f"{end - start}")
