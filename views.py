from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, Enrollment, Question, Choice, Submission


def extract_answers(request):
    submitted_anwsers = []
    for key in request.POST:
        if key.startswith('choice'):
            value = request.POST.getlist(key)
            for item in value:
                submitted_anwsers.append(int(item))
    return submitted_anwsers


@login_required
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    enrollment, _ = Enrollment.objects.get_or_create(user=user, course=course)

    submission = Submission.objects.create(enrollment=enrollment)
    choices = extract_answers(request)
    submission.choices.set(choices)
    submission.save()

    return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)


@login_required
def show_exam_result(request, course_id, submission_id):
    context = {}
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    selected_ids = submission.choices.values_list('id', flat=True)

    total_score = 0
    possible_score = 0
    for question in course.question_set.all():
        possible_score += question.grade
        if question.is_get_score(selected_ids):
            total_score += question.grade

    score_percentage = int((total_score / possible_score) * 100) if possible_score > 0 else 0

    context['course'] = course
    context['selected_ids'] = selected_ids
    context['grade'] = score_percentage
    context['submission'] = submission

    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
