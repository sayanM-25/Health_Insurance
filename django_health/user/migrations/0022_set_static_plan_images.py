from django.db import migrations


def set_static_plan_images(apps, schema_editor):
    TblInsurancePlan = apps.get_model('user', 'Tbl_insurance_plan')
    image_by_category = {
        'individual': 'plan_pic/individual-plan.svg',
        'family': 'plan_pic/family-plan.svg',
        'senior': 'plan_pic/senior-plan.svg',
    }

    for plan in TblInsurancePlan.objects.all():
        plan.Fld_Insurance_pic = image_by_category.get(
            plan.Fld_Category,
            'plan_pic/default-plan.svg',
        )
        plan.save(update_fields=['Fld_Insurance_pic'])


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0021_alter_tbl_insurance_plan_fld_insurance_pic_and_more'),
    ]

    operations = [
        migrations.RunPython(set_static_plan_images, migrations.RunPython.noop),
    ]
