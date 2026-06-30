<template>
    <div
        :class="{ 'modal-open': isOpen }"
        class="modal modal-bottom sm:modal-middle"
    >
        <div class="modal-box relative w-11/12 max-w-3xl bg-base-100 p-0 flex flex-col h-[80vh]">
            <!-- Header -->
            <div class="flex justify-between items-center p-4 border-b border-base-200">
                <h3 class="font-bold text-lg flex items-center gap-2">
                    💬 Chat with Product Owner
                </h3>
                <button
                    @click="$emit('close')"
                    class="btn btn-sm btn-circle btn-ghost"
                >
                    ✕
                </button>
            </div>

            <!-- Chat History Area -->
            <div class="flex-1 overflow-y-auto p-4 bg-base-200/30" ref="chatContainer">
                <div v-if="chatHistory.length === 0" class="text-center opacity-50 mt-10">
                    <p>No messages yet. Ask the Product Owner a question!</p>
                </div>

                <div v-for="(msg, index) in chatHistory" :key="index"
                     :class="['chat', msg.role === 'user' ? 'chat-end' : 'chat-start']">
                    
                    <div class="chat-header opacity-50 text-xs mb-1">
                        {{ msg.role === 'user' ? 'You' : 'Product Owner (TAIPO)' }}
                    </div>
                    
                    <div :class="['chat-bubble', msg.role === 'user' ? 'chat-bubble-primary' : 'chat-bubble-info']">
                        <div v-if="msg.role === 'po'" v-html="msg.content" class="prose prose-sm prose-invert max-w-none"></div>
                        <div v-else class="whitespace-pre-wrap">{{ msg.content }}</div>
                    </div>
                </div>

                <div v-if="loading && pendingQuery" class="chat chat-end mt-4">
                    <div class="chat-header opacity-50 text-xs mb-1">You</div>
                    <div class="chat-bubble chat-bubble-primary">
                        <div class="whitespace-pre-wrap">{{ pendingQuery }}</div>
                    </div>
                </div>

                <!-- Loading / Error states inline -->
                <div v-if="loading" class="chat chat-start mt-4">
                    <div class="chat-header opacity-50 text-xs mb-1">Product Owner (TAIPO)</div>
                    <div class="chat-bubble chat-bubble-info flex items-center gap-2">
                        <span class="loading loading-dots loading-sm"></span>
                        <span class="text-sm opacity-75">Thinking...</span>
                    </div>
                </div>
                
                <div v-if="error" class="alert alert-error text-sm mt-4">
                    <span>Error: {{ error }}</span>
                </div>
            </div>

            <!-- Input Area -->
            <div class="p-4 border-t border-base-200 bg-base-100">
                <div class="flex justify-between items-center mb-2 px-1">
                    <details class="dropdown dropdown-top">
                        <summary class="btn btn-xs btn-ghost text-info list-none">
                            ✨ Quick Prompts
                        </summary>
                        <div class="dropdown-content z-[2] menu p-2 shadow bg-base-100 border border-base-200 rounded-box w-64 mb-2">
                            <div v-for="t in templates" :key="t.label" class="w-full">
                                <button
                                    @click="applyTemplate(t.text)"
                                    type="button"
                                    class="btn btn-ghost btn-sm justify-start w-full font-normal"
                                >
                                    {{ t.label }}
                                </button>
                            </div>
                        </div>
                    </details>
                    <span
                        :class="query.length >= maxQueryLength ? 'text-error font-bold' : 'opacity-40'"
                        class="text-[10px] font-mono"
                    >
                        {{ maxQueryLength - query.length }} chars
                    </span>
                </div>
                
                <div class="flex gap-2">
                    <textarea
                        v-model="query"
                        @keydown.enter.prevent="handleEnter"
                        :maxlength="maxQueryLength"
                        ref="queryInput"
                        class="textarea textarea-bordered h-12 flex-1 focus:border-info leading-tight resize-none"
                        placeholder="Type your message... (Enter to send, Shift+Enter for new line)"
                        :disabled="loading"
                    ></textarea>
                    
                    <button
                        @click="submitQuery"
                        :disabled="loading || !query.trim()"
                        class="btn btn-primary h-12 w-12 p-0 rounded-xl"
                        title="Send"
                    >
                        <svg v-if="!loading" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                            <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
                        </svg>
                        <span v-else class="loading loading-spinner loading-sm"></span>
                    </button>
                </div>
                <div class="text-[10px] opacity-40 italic mt-1 px-1">
                    Note: Prompts are sent to Google Gemini API. Avoid PII.
                </div>
            </div>
        </div>
        <form method="dialog" class="modal-backdrop">
            <button @click="$emit('close')">close</button>
        </form>
    </div>
</template>

<script setup>
import { ref, watch, nextTick, computed, onMounted, onUnmounted } from 'vue';
import { marked } from 'marked';

const props = defineProps({
    isOpen: Boolean,
    loading: Boolean,
    answer: String, // Used temporarily if we append immediately
    error: String,
    task: Object,
    maxQueryLength: {
        type: Number,
        default: 1320
    }
});

const emit = defineEmits(['close', 'submit']);

const query = ref('');
const pendingQuery = ref('');
const queryInput = ref(null);
const chatContainer = ref(null);

const chatHistory = computed(() => {
    if (!props.task || !props.task.po_comments) return [];
    
    const blocks = props.task.po_comments.split('\n\n---\n\n');
    const history = [];
    
    blocks.forEach(block => {
        const qMatch = block.match(/\*\*Q:\*\* ([\s\S]*?)\n\*\*A:\*\*/);
        if (qMatch) {
            const q = qMatch[1].trim();
            const a = block.split('**A:**')[1]?.trim();
            if (q) history.push({ role: 'user', content: q });
            if (a) history.push({ role: 'po', content: marked.parse(a) });
        }
    });
    
    return history;
});

const scrollToBottom = async () => {
    await nextTick();
    if (chatContainer.value) {
        chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
    }
};

watch(() => props.isOpen, async (newVal) => {
    if (newVal) {
        query.value = '';
        await nextTick();
        queryInput.value?.focus();
        scrollToBottom();
    }
});

watch(chatHistory, () => {
    if (props.isOpen) {
        scrollToBottom();
    }
}, { deep: true });

watch(() => props.loading, (newVal) => {
    if (!newVal) {
        pendingQuery.value = '';
    }
});

const submitQuery = () => {
    if (!props.loading && query.value.trim()) {
        pendingQuery.value = query.value;
        emit('submit', query.value);
        query.value = ''; // clear input immediately
    }
};

const handleEnter = (e) => {
    if (e.shiftKey) {
        // Let it insert a new line naturally
        return;
    }
    // Submit on Enter alone
    submitQuery();
};

const templates = [
    { label: 'Explain this task', text: 'Explain what this task is about and what needs to be done.' },
    { label: 'Suggest implementation', text: 'Suggest a technical implementation plan for this task.' },
    { label: 'Generate test cases', text: 'Generate a list of test cases for this task.' },
    { label: 'Security check', text: 'Identify potential security risks associated with this task.' },
    { label: 'Code snippets', text: 'Provide code snippets to help get started with this task.' },
];

const applyTemplate = (text) => {
    query.value = text;
    if (document.activeElement instanceof HTMLElement) {
        document.activeElement.blur();
    }
    nextTick(() => {
        queryInput.value?.focus();
    });
};

const handleEsc = (e) => {
    if (e.key === 'Escape' && props.isOpen) {
        emit('close');
    }
};

onMounted(() => {
    globalThis.addEventListener('keydown', handleEsc);
});

onUnmounted(() => {
    globalThis.removeEventListener('keydown', handleEsc);
});
</script>
