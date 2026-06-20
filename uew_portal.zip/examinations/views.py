from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count
from students.models import Student
from .models import Exam, ExamResult
from .forms import ExamForm, ExamResultForm


# ============ EXAMINATION DASHBOARD ============

@login_required
def exam_dashboard(request):
    exams = Exam.objects.filter(is_active=True)
    results = ExamResult.objects.all()
    pass_rate = results.filter(is_passed=True).count() / results.count() * 100 if results.count() > 0 else 0

    context = {
        'total_exams': exams.count(),
        'total_results': results.count(),
        'pass_rate': pass_rate,
        'exams': exams[:10],
        'recent_results': results.order_by('-created_at')[:10],
    }
    return render(request, 'examinations/dashboard.html', context)


# ============ EXAM VIEWS ============

@login_required
def exam_list(request):
    exams = Exam.objects.all()
    return render(request, 'examinations/exams.html', {'exams': exams})


@login_required
def add_exam(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exam created successfully!')
            return redirect('examinations:exams')
    else:
        form = ExamForm()
    return render(request, 'examinations/add_exam.html', {'form': form})


@login_required
def exam_detail(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    results = exam.results.all()

    context = {
        'exam': exam,
        'results': results,
        'total_students': results.count(),
        'average_score': results.aggregate(Avg('marks_obtained'))['marks_obtained__avg'],
        'pass_count': results.filter(is_passed=True).count(),
    }
    return render(request, 'examinations/exam_detail.html', context)


@login_required
def enter_results(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    students = Student.objects.filter(student_class=exam.class_name)

    if request.method == 'POST':
        for student in students:
            marks = request.POST.get(f'marks_{student.id}')
            if marks:
                result, created = ExamResult.objects.get_or_create(
                    exam=exam,
                    student=student,
                    defaults={'marks_obtained': marks}
                )
                if not created:
                    result.marks_obtained = marks
                    result.save()
                result.calculate_percentage()
                result.determine_grade()

        messages.success(request, 'Results entered successfully!')
        return redirect('examinations:exam_detail', pk=exam.pk)

    results = {r.student_id: r for r in exam.results.all()}
    return render(request, 'examinations/enter_results.html', {
        'exam': exam,
        'students': students,
        'results': results
    })