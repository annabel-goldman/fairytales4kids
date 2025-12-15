import { defineCollection, z } from 'astro:content';

const storiesCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    keywords: z.string(),
    image: z.string(),
    imageAlt: z.string(),
  }),
});

export const collections = {
  stories: storiesCollection,
};

