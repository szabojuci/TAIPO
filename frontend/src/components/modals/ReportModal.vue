<template>
    <dialog class="modal" :class="{ 'modal-open': isOpen }">
        <div class="modal-box w-11/12 max-w-5xl h-[80vh] flex flex-col bg-base-100">
            <h3 class="font-bold text-2xl flex items-center gap-2 mb-4 text-primary">
                📊 Project Status Report
            </h3>

            <div v-if="loading" class="flex-1 flex flex-col items-center justify-center space-y-4">
                <span class="loading loading-bars loading-lg text-primary"></span>
                <p class="text-base-content/70 animate-pulse text-lg">AI is analyzing the board and generating report...</p>
            </div>
            
            <div v-else-if="error" class="flex-1 p-4">
                <div class="alert alert-error shadow-lg">
                    <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                    <span>{{ error }}</span>
                </div>
            </div>

            <div v-else class="flex-1 bg-base-200/50 p-6 rounded-lg overflow-y-auto prose prose-sm md:prose-base max-w-none text-base-content" v-html="renderedReport">
            </div>

            <div class="modal-action mt-6">
                <button @click="$emit('close')" class="btn btn-primary" :disabled="loading">Close</button>
            </div>
        </div>
        <form method="dialog" class="modal-backdrop">
            <button @click="$emit('close')">close</button>
        </form>
    </dialog>
</template>

<script setup>
import { computed } from 'vue';
import { marked } from 'marked';

const props = defineProps({
    isOpen: Boolean,
    report: String,
    loading: Boolean,
    error: String
});

defineEmits(['close']);

const renderedReport = computed(() => {
    if (!props.report) return '';
    return marked.parse(props.report, { breaks: true });
});
</script>
