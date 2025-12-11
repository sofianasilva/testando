import axios from "axios";
import { env } from '@/stores/env'

export const api = axios.create({
  baseURL: env.API_BASE_URL,
  headers: { 
    "Content-Type": "application/json"
  },
  withCredentials: true,
});

export interface QuestionnaireSubmission {
  questionnaire_type: string;
  answers: Record<string, { adoption: string; comment: string }>;
}

export const submitQuestionnaire = async (data: QuestionnaireSubmission) => {
  try {
    const response = await api.post('/questionnaire/submit/', data);
    return response.data;
  } catch (error) {
    console.error('Failed to submit questionnaire:', error);
    throw error;
  }
};