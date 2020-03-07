# from django import forms
# from billing.models import BillingProfile
#
#
# class BillingProfileForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(BillingProfileForm, self).__init__(*args, **kwargs)
#         instance = getattr(self, 'instance', None)
#         if instance.verify:
#             self.fields['nid'].widget.attrs['readonly'] = True
#             self.fields['full_name'].widget.attrs['readonly'] = True
#
#     class Meta:
#         model = BillingProfile
#
#         fields = (
#             'full_name', 'phone', 'nid'
#         )
#
# #
# # class BillingProfileFormVerify(forms.ModelForm):
# #     class Meta:
# #         model = BillingProfile
# #
# #         fields = (
# #             'full_name','phone'
# #         )
