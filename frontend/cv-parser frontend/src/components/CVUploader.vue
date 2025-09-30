<template>
  <div class="uploader">
    <h2>Upload CV</h2>
    <input type="file" @change="onFileChange" accept=".pdf,.docx,.pptx,.txt" />
    <button @click="uploadCV">Upload & Parse</button>

    <div v-if="parsedData" style="margin-top: 16px">
      <h3>Parsed Data</h3>

      <section>
        <strong>Name:</strong> {{ parsedData.name || '—' }}<br />
        <strong>Email:</strong> {{ parsedData.email || '—' }}<br />
        <strong>Phone:</strong> {{ parsedData.phone_number || '—' }}<br />
        <strong>Designation:</strong> {{ parsedData.designation || '—' }}<br />
        <strong>Nationality:</strong> {{ parsedData.nationality || '—' }}<br />
        <strong>Skills:</strong> {{ parsedData.skills || '—' }}
      </section>

      <section style="margin-top: 12px">
        <h4>Education</h4>
        <ul v-if="parsedData.education && parsedData.education.length">
          <li v-for="(e, i) in parsedData.education" :key="i">
            {{ e.institution }}<span v-if="e.gpa"> — GPA: {{ e.gpa }}</span>
          </li>
        </ul>
        <div v-else>—</div>
      </section>

      <section style="margin-top: 12px">
        <h4>Projects</h4>
        <ul v-if="parsedData.projects && parsedData.projects.length">
          <li v-for="(p, i) in parsedData.projects" :key="i">{{ p }}</li>
        </ul>
        <div v-else>—</div>
      </section>

      <section style="margin-top: 12px">
        <h4>Past Companies</h4>
        <ul v-if="parsedData.past_companies && parsedData.past_companies.length">
          <li v-for="(c, i) in parsedData.past_companies" :key="i">{{ c }}</li>
        </ul>
        <div v-else>—</div>
      </section>

      <details style="margin-top:12px">
        <summary>Raw JSON</summary>
        <pre>{{ parsedData }}</pre>
      </details>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'CVUploader',
  data() {
    return {
      file: null,
      parsedData: null
    };
  },
  methods: {
    onFileChange(e) {
      this.file = e.target.files[0] || null;
    },
    async uploadCV() {
      if (!this.file) {
        alert("Please select a file first.");
        return;
      }
      const formData = new FormData();
      formData.append('file', this.file);

      try {
        const { data } = await axios.post('http://127.0.0.1:5000/api/parse-cv', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        this.parsedData = data.parsed_data || data; // support either shape
      } catch (err) {
        console.error(err?.response?.data || err.message);
        alert((err?.response?.data && err.response.data.error) || "Error parsing CV");
      }
    }
  }
};
</script>
