import { ref, computed, onMounted } from 'vue'
import { submitQuestionnaire, type QuestionnaireSubmission } from '@/services/api'

export type Q = { id: string; code: string; text: string }
export type A = { adoption: string; comment: string }

export function useQuestionnaire(QUESTIONS: Q[], questionnaireType: string) {
  const questions = ref<Q[]>([])
  const answers = ref<Record<string, A>>({})
  const isSubmitting = ref(false)
  const submitError = ref<string | null>(null)
  const submitSuccess = ref(false)

  onMounted(() => {
    questions.value = QUESTIONS ?? []
    for (const q of questions.value) {
      answers.value[q.id] = { adoption: '', comment: '' }
    }
  })

  const half = computed(() => Math.ceil(questions.value.length / 2))
  const left = computed(() => questions.value.slice(0, half.value))
  const right = computed(() => questions.value.slice(half.value))

  const dump = () => JSON.parse(JSON.stringify(answers.value))

  const submit = async () => {
    isSubmitting.value = true
    submitError.value = null
    submitSuccess.value = false

    try {
      const submission: QuestionnaireSubmission = {
        questionnaire_type: questionnaireType,
        answers: answers.value
      }

      const result = await submitQuestionnaire(submission)
      console.log('Questionnaire submitted successfully:', result)
      submitSuccess.value = true
      
      // Reset form after successful submission
      for (const q of questions.value) {
        answers.value[q.id] = { adoption: '', comment: '' }
      }
      
      return result
    } catch (error: any) {
      console.error('Failed to submit questionnaire:', error)
      submitError.value = error.response?.data?.error || 'Failed to submit questionnaire'
      throw error
    } finally {
      isSubmitting.value = false
    }
  }

  return { 
    questions, 
    answers, 
    left, 
    right, 
    dump, 
    submit,
    isSubmitting,
    submitError,
    submitSuccess
  }
}
