<template>
    <div
        v-if="isOpen"
        class="fixed inset-0 bg-neutral/60 backdrop-blur-sm overflow-y-auto h-full w-full z-50 flex items-center justify-center p-4 transition-all duration-300"
        @click.self="$emit('close')"
    >
        <div class="relative w-full max-w-3xl bg-base-100 shadow-2xl rounded-2xl overflow-hidden animate-in fade-in zoom-in duration-200 flex flex-col max-h-[90vh]">
            <div class="px-6 py-4 border-b border-base-300 flex items-center justify-between bg-base-200 shrink-0">
                <h3 class="text-xl font-bold flex items-center gap-2">
                    ☕ Daily Standup (Scrum)
                </h3>
                <button
                    @click="$emit('close')"
                    class="btn btn-ghost btn-sm btn-circle"
                >
                    ✕
                </button>
            </div>
            
            <div class="p-6 prose prose-base max-w-none text-base-content overflow-y-auto" v-html="formattedContent">
            </div>

            <div class="px-6 py-4 border-t border-base-300 bg-base-200 flex justify-end shrink-0">
                <button @click="$emit('close')" class="btn btn-primary">Got it!</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue';
import { marked } from 'marked';

const props = defineProps({
    isOpen: {
        type: Boolean,
        default: false
    },
    content: {
        type: String,
        default: ''
    }
});

defineEmits(['close']);

const formattedContent = computed(() => {
    if (!props.content) return '<p class="opacity-50 italic">Generating standup...</p>';
    return marked.parse(props.content);
});
</script>
