from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('home', views.index, name='home'),
    path('login', views.loginPage, name='login'),
    path('register', views.userRegister, name='register'),
    path('logout', views.logoutUser, name='logout'),
    path('not_verified', views.not_verified, name='not_verified'),
    path('user_profile/<int:user_id>', views.userProfile, name='user_profile'),
    path('item_description/<int:item_id>', views.itemDescription, name='item_description'),

    path('issues_raised', views.issues_raised,name='issues_raised'),
    path('view_issue/<int:issue_id>', views.view_issue,name='view_issue_'),
    path('close_issue/<int:issue_id>', views.close_issue,name='close_issue_'),

    path('issue_approve/<int:issue_id>', views.issue_approve, name='issue_approve'),
    path('issue_reject/<int:issue_id>', views.issue_reject, name='issue_reject'),

    
    path('organiser_requests', views.organiser_requests, name='organiser_requests'),
    path('supplier_requests', views.supplier_requests, name='supplier_requests'),
    path('researcher_requests', views.researcher_requests, name='researcher_requests'),
    path('raised_issues', views.raised_issues, name='raised_issues'),
    path('donations', views.donations, name='donations'),

    path('organiser_requests_approve/<int:organiser_id>', views.organiser_request_approve, name='organiser_requests_approve'),
    path('organiser_requests_reject/<int:organiser_id>', views.organiser_request_reject, name='organiser_requests_reject'),
    path('supplier_requests_approve/<int:supplier_id>', views.supplier_request_approve, name='supplier_requests_approve'),
    path('supplier_requests_reject/<int:supplier_id>', views.supplier_request_reject, name='supplier_requests_reject'),
    path('researcher_requests_approve/<int:researcher_id>', views.researcher_request_approve, name='researcher_requests_approve'),
    path('researcher_requests_reject/<int:researcher_id>', views.researcher_request_reject, name='researcher_requests_reject'),


    path('volunteer', views.volunteer, name='volunteer'),
    path('raise_issues', views.raise_issues, name='raise_issues'),
    path('resources',views.resources, name='resources'),
    path('marketPlace', views.marketPlace, name='marketPlace'),
    path('donate', views.donate, name='donate'),

    path('register_event/<int:event_id>', views.register_event, name='register_event_'),
    path('unregister_event/<int:event_id>', views.unregister_event, name='unregister_event_'),
    path('buy_item/<int:item_id>', views.buy_item, name='buy_item_'),
    path('order',views.active_orders, name='orders_'),
    path('cancel_order/<int:order_id>',views.cancel_order, name='cancel_order_'),
    path('payment_cancelled',views.payment_cancelled, name='payment_cancelled_'),
    path('payment_success',views.payment_success, name='payment_success_'),
    

    path('organiser_event', views.organise_event, name='organise_event'),
    path('manage_volunteers', views.manage_volunteers, name='manage_volunteers'),

    path('manage_volunteer_details/<int:event_id>', views.manage_volunteer_details, name='manage_volunteer_details'),
    path('remove_volunteer/<int:volunteer_id>', views.remove_volunteer, name='remove_volunteer'),

    
    path('orders', views.orders,name='orders'),
    path('list_items', views.list_items, name='list_items'),

    path('cancelled_orders', views.cancelled_orders, name='cancelled_orders'),
    path('return_pay/<int:order_id>', views.return_pay, name='return_pay'),
    path('add_item', views.add_item, name='add_item_'),
    path('edit_item/<int:item_id>', views.edit_item, name='edit_item'),
    path('delete_item/<int:item_id>', views.delete_item, name='delete_item'),
    path('order_delivered/<int:order_id>', views.order_delivered, name='order_delivered'),

    
    path('publish_paper', views.publish_paper, name='publish_paper'),
    path('manage_resources', views.manage_resources, name='manage_resources'),

    path('delete_resources/<int:resource_id>', views.delete_resource, name='delete_resource'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)