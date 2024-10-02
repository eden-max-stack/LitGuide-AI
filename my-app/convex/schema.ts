// convex/schema.ts
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  messages: defineTable({
    author: v.string(),
    message: v.any(),
  }),

  keywords: defineTable({
    keyword: v.string(),
  }),
});

