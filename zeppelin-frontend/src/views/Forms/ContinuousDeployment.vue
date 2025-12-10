<template>
  <AdminLayout>
    <PageBreadcrumb :pageTitle="pageTitle" />

    <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
      <div class="space-y-6">
        <ComponentCard :title="pageTitle">
          <div class="space-y-4 dark:text-white">
            <QuestionItem
              v-for="q in left"
              :key="q.id"
              :question="q"
              v-model:adoption="answers[q.id].adoption"
              v-model:comment="answers[q.id].comment"
            />
          </div>
        </ComponentCard>
      </div>

      <div class="space-y-6">
        <ComponentCard title="continuação">
          <div class="space-y-4 dark:text-white">
            <QuestionItem
              v-for="q in right"
              :key="q.id"
              :question="q"
              v-model:adoption="answers[q.id].adoption"
              v-model:comment="answers[q.id].comment"
            />
          </div>
        </ComponentCard>

        <div class="space-y-4">
          <!-- Success Message -->
          <div v-if="submitSuccess" class="p-4 bg-green-100 border border-green-400 text-green-700 rounded">
            Questionário enviado com sucesso!
          </div>
          
          <!-- Error Message -->
          <div v-if="submitError" class="p-4 bg-red-100 border border-red-400 text-red-700 rounded">
            {{ submitError }}
          </div>
          
          <div class="flex justify-end">
            <button 
              class="px-4 py-2 bg-brand-950 text-white rounded-lg hover:bg-brand-900 disabled:opacity-50 disabled:cursor-not-allowed" 
              @click="submit"
              :disabled="isSubmitting"
            >
              {{ isSubmitting ? 'Enviando...' : 'Salvar' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import ComponentCard from '@/components/common/ComponentCard.vue'
import QuestionItem from './QuestionItem.vue'

import QUESTIONS from '@/data/continuous_deployment.json'
import { useQuestionnaire } from '@/composables/useQuestionnaire'

const pageTitle = 'Continuous Deployment'
const { answers, left, right, submit, isSubmitting, submitError, submitSuccess } = useQuestionnaire(QUESTIONS as any, 'continuous_deployment')
</script>
