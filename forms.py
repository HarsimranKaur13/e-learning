from django import forms
from django.forms import SelectDateWidget, RadioSelect
from myapp.models import Student,Order
YESNO=[(0,'No'),(1,'Yes')]
class OrderForm(forms.ModelForm):
    class Meta:
        model=Order
        fields="__all__"
        student=forms.ModelChoiceField(widget=RadioSelect,queryset=Student.objects.all())
        course=forms.CharField()
        levels=forms.IntegerField()
        order_date=forms.DateField(widget=SelectDateWidget)
class InterestForm(forms.Form):
    interested=forms.ChoiceField(widget=forms.RadioSelect,choices=YESNO)
    levels=forms.IntegerField(min_value=1,initial=1)
    comments=forms.CharField(widget=forms.Textarea(attrs={'required':False,'label':'Additional Comments'}))
class RegisterForm(forms.ModelForm):
    class Meta:
        model=Student
        fields = ('username','password','first_name','last_name','city','interested_in')
        username = forms.CharField(widget=forms.Textarea(attrs={'label':'Username'}))
        password = forms.CharField(widget=forms.Textarea(attrs={'label':'Password'}))
        first_name = forms.CharField(widget=forms.Textarea(attrs={'label':'Firstname'}))
        last_name = forms.CharField(widget=forms.Textarea(attrs={'label':'Lastname'}))
        city = forms.CharField(widget=forms.Textarea(attrs={'label':'City'}))
        interested_in = forms.CharField(widget=forms.Textarea(attrs={'label':'Interested in'}))


