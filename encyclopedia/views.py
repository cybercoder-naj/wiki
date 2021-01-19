from random import randint

from django import forms
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from markdown2 import markdown

from . import util


class NewPageForm(forms.Form):
    title = forms.CharField(label='Title')
    content = forms.CharField(label='Content')


class SearchForm(forms.Form):
    q = forms.CharField()


def index(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        q = form.cleaned_data['q']
        print(q)
        entries = util.list_entries()
        for entry in entries:
            if entry.upper() == q.upper():
                return HttpResponseRedirect(reverse('encyclopedia:entry_page', kwargs={
                    'title': entry
                }))
        list_entries = list()
        for entry in entries:
            if q in entry:
                list_entries.append(entry)
                return render(request, 'encyclopedia/index.html', {
                    'entries': list_entries
                })
    else:
        return render(request, 'encyclopedia/index.html', {
            "entries": util.list_entries()
        })


def entry_page(request, title):
    md_text = util.get_entry(title)
    if md_text is not None:
        html = markdown(md_text)
        return render(request, 'encyclopedia/entry.html', {
            'title_name': title,
            'content': html
        })
    else:
        return render(request, 'encyclopedia/404.html')


def new_page(request):
    if request.method == 'GET':
        return render(request, 'encyclopedia/new_page.html', {
            'form': NewPageForm(),
            'edit': False
        })
    else:
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            if util.get_entry(title) is None:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse('encyclopedia:entry_page', kwargs={
                    'title': title
                }))
            else:
                messages.error(request, 'Title Already Exists!')
                return render(request, 'encyclopedia/new_page.html', {
                    'form': form,
                    'edit': False
                })
        else:
            return render(request, 'encyclopedia/new_page.html', {
                'form': form,
                'edit': False
            })


def edit_page(request, title):
    if request.method == 'POST':
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('encyclopedia:entry_page', kwargs={
                'title': title
            }))
        else:
            return render(request, 'encyclopedia/new_page.html', {
                'form': form,
                'edit': True
            })
    else:
        content = util.get_entry(title)
        form = NewPageForm(initial={
            'title': title,
            'content': content,
        })
        return render(request, 'encyclopedia/new_page.html', {
            'form': form,
            'edit': True
        })


def random_page(request):
    entries = util.list_entries()
    position = randint(0, len(entries) - 1)
    return HttpResponseRedirect(reverse('encyclopedia:entry_page', kwargs={
        'title': entries[position]
    }))