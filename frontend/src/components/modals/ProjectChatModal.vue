<template>
    <div
        v-if="isOpen"
        @click.self="$emit('close')"
        class="fixed inset-0 bg-neutral/60 backdrop-blur-sm overflow-y-auto h-full w-full z-[100] flex items-center justify-center p-4"
    >
        <div class="relative w-full max-w-2xl bg-base-100 rounded-2xl shadow-2xl flex flex-col max-h-[80vh] overflow-hidden">
            <!-- Header -->
            <div class="px-6 py-4 border-b border-base-300 flex justify-between items-center bg-base-200/50">
                <h3 class="text-xl font-bold flex items-center gap-2">
                    <span class="text-2xl">🤖</span> Ask Project PO
                </h3>
                <button @click="$emit('close')" class="btn btn-ghost btn-sm btn-circle">✕</button>
            </div>

            <!-- Chat Area -->
            <div class="p-6 overflow-y-auto flex-grow bg-base-100 flex flex-col gap-4 min-h-[300px]">
                <div v-if="messages.length === 0" class="text-center text-base-content/50 mt-10">
                    <p class="text-lg font-semibold">Hello! I am the AI Product Owner.</p>
                    <p class="text-sm">Ask me anything about the "{{ projectName }}" domain, architecture, or requirements.</p>
                </div>
                
                <div v-for="(msg, index) in messages" :key="index" :class="['chat', msg.role === 'user' ? 'chat-end' : 'chat-start']">
                    <div class="chat-image avatar">
                        <div class="w-10 rounded-full bg-base-300 flex items-center justify-center text-xl">
                            {{ msg.role === 'user' ? '👤' : '🤖' }}
                        </div>
                    </div>
                    <div class="chat-header text-xs opacity-50 mb-1">
                        {{ msg.role === 'user' ? 'You' : 'Project PO' }}
                    </div>
                    <div :class="['chat-bubble prose prose-sm max-w-none text-base-content', msg.role === 'user' ? 'chat-bubble-primary text-primary-content' : 'chat-bubble-base-200 border border-base-300 bg-base-100']" v-html="formatMessage(msg.content)">
                    </div>
                </div>

                <div v-if="loading" class="chat chat-start">
                    <div class="chat-image avatar">
                        <div class="w-10 rounded-full bg-base-300 flex items-center justify-center text-xl">🤖</div>
                    </div>
                    <div class="chat-bubble bg-base-100 border border-base-300">
                        <span class="loading loading-dots loading-sm"></span>
                    </div>
                </div>
            </div>

            <!-- Input Area -->
            <div class="p-4 border-t border-base-300 bg-base-200/50">
                <form @submit.prevent="sendMessage" class="flex gap-2">
                    <input
                        v-model="query"
                        type="text"
                        placeholder="Ask about project features, tech stack, or business rules..."
                        class="input input-bordered flex-grow focus:ring-2 focus:ring-primary/50"
                        :disabled="loading"
                    />
                    <button type="submit" class="btn btn-primary" :disabled="!query.trim() || loading">
                        Send
                    </button>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { marked } from 'marked';
import { api } from '../../services/api.js';

const props = defineProps({
    isOpen: Boolean,
    projectName: String
});

const emit = defineEmits(['close']);

const query = ref('');
const messages = ref([]);
const loading = ref(false);

watch(() => props.isOpen, (newVal) => {
    if (newVal) {
        messages.value = [];
        query.value = '';
    }
});

const formatMessage = (text) => {
    return marked.parse(text);
};

const sendMessage = async () => {
    if (!query.value.trim() || loading.value) return;

    const userQuery = query.value.trim();
    messages.value.push({ role: 'user', content: userQuery });
    query.value = '';
    loading.value = true;

    try {
        const res = await api.queryProject(props.projectName, userQuery);
        if (res.success) {
            messages.value.push({ role: 'assistant', content: res.answer });
        } else {
            messages.value.push({ role: 'assistant', content: 'Error: ' + res.error });
        }
    } catch (err) {
        messages.value.push({ role: 'assistant', content: 'Server Error: ' + err.message });
    } finally {
        loading.value = false;
    }
};
</script>
