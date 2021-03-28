from django import template

register = template.Library()


@register.filter
def ru_pluralize(value_to_pluralize, arg="дурак,дурака,дураков"):  # noqa: CCR001
    args = arg.split(",")
    number = abs(int(value_to_pluralize))
    tens = number % 10
    hundrends = number % 100

    if (tens == 1) and (hundrends != 11):
        return f"{number} {args[0]}"
    elif (tens >= 2) and (tens <= 4) and ((hundrends < 10) or (hundrends >= 20)):
        return f"{number} {args[1]}"
    else:
        return f"{number} {args[2]}"
