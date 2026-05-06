import api from './api';

export async function getQuestions() {
  const response = await api.get('/questionnaires/questions');
  return response.data;
}

export async function submitResponses(answers) {
  const response = await api.post('/questionnaires/responses', answers);
  return response.data;
}

