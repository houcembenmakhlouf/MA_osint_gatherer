from wtforms import Form, StringField, SelectField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class JobForm(Form):
    job = SelectField(
        "Job Type",
        validators=[DataRequired()],
        choices=[
            ("twitter.profile", "twitter.profile"),
            ("twitter.followers", "twitter.followers"),
            ("twitter.tweets", "twitter.tweets"),
            ("twitter.likers", "twitter.likers"),
            ("twitter.retweeters", "twitter.retweeters"),
            ("twitter.replies", "twitter.replies"),
            ("twitter.quotes", "twitter.quotes"),
            ("example.sleep_fixed", "example.sleep_fixed"),
            ("example.sleep_time", "example.sleep_time"),
        ],
    )
    args = StringField("Args")


class ScheduledJobForm(JobForm):
    interval = IntegerField(
        "Interval (min)", default=10, validators=[NumberRange(min=1, max=1440)]
    )
    repeat = IntegerField("Repeat (0=forever)", default=0)
