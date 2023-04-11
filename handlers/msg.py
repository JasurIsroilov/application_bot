from dataclasses import dataclass


@dataclass
class CrewMsg:
    """
    The set of messages
    """
    main_menu = 'Здравствуйте! Выберите действие!'

    support_menu = 'Выберите вид услуги'

    support_task = 'Опишите задачу в свободной форме'

    support_trouble = 'Опишите проблему в свободной форме'

    hr = 'Опишите текст заявки в свободной форме'

    hr_newcomer = 'Опишите задачу в свободной форме'

    hr_firing = 'Опишите задачу в свободной форме'

    msg_header = 'ФИО: {}\n' \
                 'Номер: {}\n' \
                 'Телеграм: @{}\n' \
                 'Отдел: {}\n\n' \
                 '<b>Задача:</b>\n'
