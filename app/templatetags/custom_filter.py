from django import template

register = template.Library()


@register.filter
def get_time_slot_availability(value, key):
    formatted_key = key.strftime("%H:%M")
    return value.get(formatted_key, False)


@register.filter
def get_date_availability(dictionary, date):
    formatted_date = date.strftime("%Y-%m-%d")
    return dictionary.get(formatted_date, {})


@register.filter()
def get_item(dictionary, key):
    return dictionary.get(key)
