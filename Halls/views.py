from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import Halls, Shar, Client
from .forms import SharForm, HallForm
from django.views.generic import ListView
from django.views.decorators.http import require_POST
from django.contrib.auth import logout
from django.contrib import messages

# قائمة بعرض جميع القاعات (استخدام الكلاس المعتمد على ListView)
class HallsListView(ListView):
    model = Halls
    template_name = 'halls/post/halls_list.html'
    context_object_name = 'halls'
    paginate_by = 3  
    ordering = ['-created']  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['sidebar_halls'] = Halls.objects.filter(active=True).order_by('-created')[:10]
        return context


# دالة عرض تفاصيل القاعة
def halls_detail(request, slug):
    halls = get_object_or_404(Halls, slug=slug)
    shar = halls.shar.filter(active=True)
    form = SharForm()
    
    sidebar_halls = Halls.objects.filter(active=True).order_by('-created')[:5]  

    return render(request, 'halls/post/detail.html', {
        'halls': halls,
        'shar': shar,
        'form': form,
        'sidebar_halls': sidebar_halls,  
    })


# دالة لإضافة تعليق على قاعة محددة
@require_POST
def halls_shar(request, halls_id):
    halls = get_object_or_404(Halls, id=halls_id, active=True)
    form = SharForm(data=request.POST)
    if form.is_valid():
        shar = form.save(commit=False)
        shar.halls = halls
        shar.save()
        return redirect('halls:halls_detail', slug=halls.slug)

    shar_list = halls.shar.filter(active=True)
    return render(request, 'halls/post/detail.html', {
        'halls': halls,
        'form': form,
        'shar': shar_list
    })


# عرض القاعات الخاصة بعميل محدد (استخدام الكلاس المعتمد على ListView)
class ClientHallsListView(ListView):
    model = Halls
    template_name = 'halls/post/client.html'
    context_object_name = 'halls'

    # جلب بيانات العميل من الجلسة
    def get_queryset(self):
        client = get_object_or_404(Client, id=self.request.session.get('client_id'))
        return Halls.objects.filter(client=client)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client = get_object_or_404(Client, id=self.request.session.get('client_id'))
        context['client'] = client  # تمرير بيانات العميل إلى القالب
        return context

# دالة إنشاء حساب جديد أو تسجيل الدخول
def sign_up(request):
    if request.method == 'POST':
        if 'signup' in request.POST:  # إذا كان المستخدم يريد إنشاء حساب جديد
            name = request.POST.get('name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            phone = request.POST.get('phone')

            if name and email and password and phone:
                client = Client.objects.create(
                    name=name,
                    email=email,
                    password=make_password(password),
                    phone=phone,
                )
                client.save()
                return redirect('halls:sign_up')

        elif 'login' in request.POST:   # إذا كان المستخدم يريد تسجيل الدخول
            email = request.POST.get('email')
            password = request.POST.get('password')

            try:
                client = Client.objects.get(email=email)
                if client.check_password(password):  # التحقق من كلمة المرور
                    # تخزين بيانات العميل في session لتسجيل دخوله
                    request.session['client_id'] = client.id
                    return redirect('halls:client_list')  
                else:
                    return render(request, 'halls/post/sign_up.html', {'error': 'كلمة السر غير صحيحة'})
            except Client.DoesNotExist:
                return render(request, 'halls/post/sign_up.html', {'error': 'البريد الإلكتروني غير موجود'})

    return render(request, 'halls/post/sign_up.html')

#تسجيل الخروج
def logout_view(request):
    logout(request)
    return redirect('halls:sign_up')


# دالة حذف قاعة من جدول العميل او القالب تبعة
def halls_delete(request, id):
    if request.method == "POST":
        hall = get_object_or_404(Halls, id=id)
        hall.delete()
        return redirect('halls:client_list')

# دالة إضافة قاعة جديدة
def halls_add(request):
    if request.method == 'POST':
        form = HallForm(request.POST, request.FILES)
        if form.is_valid():
            hall = form.save(commit=False)
            hall.client = get_object_or_404(Client, id=request.session.get('client_id'))
            hall.save()
            return redirect('halls:client_list')
    else:
        form = HallForm()
    return render(request, 'halls/post/halls_form.html', {'form': form})

# دالة تعديل بيانات قاعة
def halls_edit(request, pk):
    hall = get_object_or_404(Halls, pk=pk)
    if request.method == 'POST':
        form = HallForm(request.POST, request.FILES, instance=hall)
        if form.is_valid():
            form.save()
            return redirect('halls:client_list')
    else:
        form = HallForm(instance=hall)
    return render(request, 'halls/post/halls_form.html', {'form': form})




# دالة تعديل بيانات العميل
def edit_client(request):
    client = get_object_or_404(Client, id=request.session.get('client_id'))

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')

    # التحقق من صحة كلمة المرور القديمة 
        if client.check_password(old_password):
            client.name = name
            client.email = email
            client.phone = phone

            if new_password:
                client.set_password(new_password)
            
            client.save()
            messages.success(request, "تم تعديل بياناتك بنجاح.")
            return redirect('halls:client_list')
        else:
            messages.error(request, "كلمة المرور الحالية غير صحيحة.")

    return render(request, 'halls/post/edit_client.html', {'client': client})
